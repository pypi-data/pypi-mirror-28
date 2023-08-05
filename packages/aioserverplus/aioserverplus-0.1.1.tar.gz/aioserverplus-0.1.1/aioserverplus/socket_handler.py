import asyncio
import json
import logging
from abc import abstractmethod
from concurrent.futures import CancelledError

import aiohttp.web as web

from .handler import BaseHandler

log = logging.getLogger('aioserverplus')


async def socket_response(generator, request, *args, **kwargs):
    """
    Socket response for streaming data from a generator
    :param generator: function -> non blocking generator -> yields dictionary or None (when requesting socket write)
    :param request: request object received by normal api method
    :param args: arguments for generator (optional)
    :param kwargs: keyword arguments for generator (optional)
    :return:
    """
    response = web.StreamResponse(status=200)
    await response.prepare(request)
    try:
        for result in generator(*args, **kwargs):
            await asyncio.sleep(0)
            if result is None:
                await response.drain()
                continue
            chunk = bytes(json.dumps(result), encoding='utf8')
            response.write(chunk + b'\n')
            log.debug('Wrote to buffer: %s', str(chunk))
        await response.write_eof()
        return response
    except CancelledError:
        log.debug('Socket at %s has disconnected', request.ip_port)
        return response


class SocketHandler(BaseHandler):
    def __init__(self, *args, **kwargs):
        if args and isinstance(args[0], dict):
            super(SocketHandler, self).__init__(*args[1:], **kwargs)
            self.bind_handlers(args[0])
        else:
            super(SocketHandler, self).__init__(*args, **kwargs)
        self.running = True
        self._clients = {}
        self.authenticated_users = set()

    @abstractmethod
    async def load_sources(self):
        raise NotImplementedError

    @abstractmethod
    def parse_sources(self, request):
        raise NotImplementedError

    @abstractmethod
    async def get_data(self, source):
        raise NotImplementedError

    def _new_connection(self, request):
        sources = self.parse_sources(request)
        log.debug('New client %s has requested %s: %s', request.ip_port, request.pth, str(sources))
        self._clients[request.ip_port] = (asyncio.Queue(), [])
        for source in sources:
            self._clients[request.ip_port][1].append(source)

    def _remove_connection(self, request):
        log.debug('Client %s has disconnected', request.ip_port)
        del self._clients[request.ip_port]

    def _queue_generator(self, client):
        while self.running:
            try:
                yield self._clients[client][0].get_nowait()
            except asyncio.QueueEmpty:
                yield None

    async def handle_request(self, request):
        if request.pth in self.handlers:
            log.debug('Serving static request, %s', request.pth)
            return await self.handlers[request.pth](request)
        else:
            self._new_connection(request)
            response = await socket_response(self._queue_generator, request, request.ip_port)
            self._remove_connection(request)
            return response

    async def _serve_source(self, source):
        while self.running:
            # Yield control to loop in case get_data does not
            await asyncio.sleep(0)
            data = await self.get_data(source)
            for client, (queue, sources) in self._clients.items():
                count = 0
                for src in sources:
                    if src == source:
                        count += 1
                        await queue.put(data)
                if count:
                    log.debug('Distributing %s to %d connected clients', str(source), count)

    async def backend(self):
        jobs = []
        sources = await self.load_sources()
        for source in sources:
            jobs.append(self._serve_source(source))
        await asyncio.gather(*jobs)
