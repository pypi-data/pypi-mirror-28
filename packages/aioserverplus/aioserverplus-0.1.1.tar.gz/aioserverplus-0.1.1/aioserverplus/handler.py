import asyncio
import logging
from abc import ABC, abstractmethod
from collections import defaultdict
from datetime import datetime
from functools import partial
from hashlib import sha1
from time import time

import aiohttp.web as web

log = logging.getLogger('aioserverplus')


class BaseHandler(ABC):
    """
    Abstract class for all handlers that implements rate limiting and authentication of requests
    """
    def __init__(self, interval=None, req_per_interval=None, blacklist=None):
        """
        :param interval: length of rate limit interval (seconds)
        :param req_per_interval: number of requests allowed in given interval
        :param blacklist: number of requests above rate limit to blacklist an ip
        """
        self.clients = {}
        self.blacklist = set()
        self.connections_over_limit = {}
        self.authenticated_users = {}
        self.interval = interval or 1
        self.req_per_interval = req_per_interval or 10000
        self.n_to_blacklist = blacklist or 10000

        self.handlers = {}

    def bind_handlers(self, handlers):
        """If handler function has 'self' as an argument, then bind to current handler class"""
        for k, v in handlers.items():
            try:
                assert 'self' in v.__code__.co_varnames
                self.handlers[k] = partial(v, self)
            except (AssertionError, AttributeError):
                self.handlers[k] = v

    def reset_rate_limit(self, ip):
        """
        Resets rate limit and connections over limit for a given ip
        :param: ip: ip address of connection
        """
        self.clients[ip] = {'start': int(time()), 'n_requests': 0}
        self.connections_over_limit[ip] = 0

    def allowed_to_connect(self, ip, key):
        """
        Checks whether an ip-key pair is allowed to access resource
        :param ip: ip-address of request - "ip:port"
        :param key: api-key of request
        :return: tuple:(request_is_rate_limited, request_is_authenticated)
        """
        if ip in self.blacklist:
            log.debug('{} Request blacklisted'.format(ip))
            return False, False

        if ip not in self.clients:
            log.debug('{} New connection'.format(ip))
            self.reset_rate_limit(ip)

        return self.rate_limit(ip), self.authenticate(key)

    def rate_limit(self, ip):
        """
        Checks if ip is over rate limit and adds ip to blacklist if too many requests over the limit have been made
        :param ip: ip-address of request - "ip:port"
        :return: bool:request_is_rate_limited
        """
        if int(time()) >= self.clients[ip]['start'] + self.interval:
            self.clients[ip] = {'start': int(time()), 'n_requests': 0}
            self.connections_over_limit[ip] = 0

        self.clients[ip]['n_requests'] += 1

        if self.clients[ip]['n_requests'] <= self.req_per_interval:
            log.debug('{:15s} Under rate limit, %4d / %4d'.format(ip),
                      self.clients[ip]['n_requests'], self.req_per_interval)
            return True
        else:
            log.debug('{:15s} Over rate limit, %4d / %4d, %d'.format(ip),
                      self.clients[ip]['n_requests'], self.req_per_interval, self.connections_over_limit[ip])
            self.connections_over_limit[ip] += 1
            if self.connections_over_limit[ip] >= self.n_to_blacklist:
                self.blacklist.add(ip)
                log.info('{} Connection blacklisted'.format(ip))
            return False

    def authenticate(self, key):
        """
        Checks whether sha1 hash of key is in authenticated users
        :param key: api-key of request
        :return: bool:request_is_authenticated
        """
        if key is None:
            log.debug('No apiKey provided')
            return False
        auth = sha1(key.encode()).hexdigest() in self.authenticated_users
        if auth:
            log.debug('%s%s Authorized connection', key, ' '*(15-len(key)))
        else:
            log.debug('%s%s Unauthorized connection', key, ' '*(15-len(key)))
        return auth

    @staticmethod
    def _patch_request(request):
        """
        Adds some useful variables onto request class for easy access
        :param request: web.Request instance
        :return: modified web.Request instance
        """
        request.ip, request.port, *_ = request.transport.get_extra_info('peername')
        request.ip_port = '{}:{}'.format(request.ip, request.port)
        request.key = request.query.get('apiKey', None)
        request.pth = str(request.rel_url).split('?')[0]
        request.params = defaultdict(lambda: None)
        request.params.update({k: request.query[k] for k in request.query.keys()})
        return request

    async def __call__(self, request):
        request = self._patch_request(request)
        status, text = 404, 'Error: Incorrect request'
        under_rate_limit, authenticated = self.allowed_to_connect(request.ip, request.key)
        local = any(request.ip.startswith(pre) for pre in ['192.168.1', '192.168.0', 'localhost', '::1', '127.0.0'])
        authenticated = authenticated or local
        if authenticated and under_rate_limit:
            log.debug('{:15s} Request successful!'.format(request.ip))
            status = 200
        elif authenticated and not under_rate_limit:
            wait = self.clients[request.ip]['start'] + self.interval - int(time())
            status, text = 403, 'Error: rate limit exceeded, try again in %f seconds' % wait
        elif not authenticated:
            status, text = 401, 'Error: Unauthorized access'
        to_log = ('[ %-15s - %-15s ] %-6s %-10s %-3d  %s', datetime.utcnow().strftime('%Y-%m-%d %I:%M:%S'), request.ip, request.method, request.pth, status, 'params = {' + ', '.join(['{}: {}'.format(k, request.params[k]) for k in sorted(list(request.params.keys()))]) + '}')
        if local:
            log.debug(*to_log)
        else:
            log.info(*to_log)
        if status != 200:
            return web.Response(text=text, status=status)
        else:
            try:
                res = await self.handle_request(request)
                # If handle function returns string then it is converted to Response with the string as text
                return res if isinstance(res, web.StreamResponse) else web.Response(text=str(res), status=200)
            except Exception as e:
                return web.Response(status=400, text='Error occurred during handling of request - %s' % repr(e))

    @abstractmethod
    async def handle_request(self, request):
        raise NotImplementedError

    async def backend(self):
        while True:
            await asyncio.sleep(10)


class Handler(BaseHandler):
    def __init__(self, handlers, interval=None, req_per_interval=None, blacklist=None):
        """
        :param handlers: dictionary of routes and handlers
            e.g. {'/': handle1, '/info': handle2}
                where handle1 and handle2 are async functions that:
                    - take (self, ) web.Request as input
                    - return web.Response or str/bytes as output
        :param interval: length of rate limit interval (seconds)
        :param req_per_interval: number of requests allowed in given interval
        :param blacklist: number of requests above rate limit to blacklist an ip
        """
        super(Handler, self).__init__(interval, req_per_interval, blacklist)
        self.authenticated_users = set()
        self.bind_handlers(handlers)

    async def handle_request(self, request):
        if request.pth in self.handlers:
            return await self.handlers[request.pth](request)
        else:
            return web.Response(status=404, text='Error: Incorrect request')
