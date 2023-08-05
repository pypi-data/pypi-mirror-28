import asyncio
import logging
import sys
from functools import partial
from time import time

from aiohttp.web import Server

from .handler import Handler
from .socket_handler import SocketHandler, socket_response


async def basic_backend(_):
    """Use backend to setup state on server that somehow cannot be done from within the class, i.e to spawn threads"""
    await asyncio.sleep(10)


async def basic_handler(_):
    """Basic request handler, returns string"""
    return 'Hello World!'


def basic_socket_generator(write_every=0.5):
    """Basic socket generator, yields data every 0.1 seconds for 30 seconds"""
    start, write_every, last_write = time(), write_every, 0
    while time() - start < 100:
        if time() - last_write > write_every:
            last_write = time()
            yield {'data': 'Hello World!'}
        else:
            yield None


def _setup_log(log_level, names, log_format='%(levelname)-5s: %(name)-15s: %(message)s'):
    """
    Sets up local logging for server for all children modules provided
    :param log_level:
    :param names:
    :param log_format: (optional)
    :return:
    """
    root_log = logging.getLogger()
    root_log.setLevel('CRITICAL')
    for h in root_log.handlers:
        root_log.removeHandler(h)

    for name in names:
        log = logging.getLogger(name)
        log.setLevel(log_level)
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(log_level)
        formatter = logging.Formatter(fmt=log_format)
        stream_handler.setFormatter(formatter)
        log.addHandler(stream_handler)


async def _async_serve(address, backend, backend_init, backend_shutdown, handler, loop):
    server = Server(handler)
    sock = await loop.create_server(server, *address)

    if backend_init is not None:
        await backend_init(handler)

    if backend is not None:
        await asyncio.gather(backend(handler), handler.backend())
    else:
        await handler.backend()

    if backend_shutdown is not None:
        await backend_shutdown(handler)

    sock.close()
    await server.shutdown()


def serve(address=('localhost', 9999), log_level='INFO', log_modules=('aioserverplus',),
          handler=Handler, handler_args=(), handler_type='default',
          backend=basic_backend, backend_init=None, backend_shutdown=None,
          interval=0, req_per_interval=0, blacklist=0):
    """
    Serves a custom handler on provided address
    :param address: tuple:(ip, port) on which to serve
    :param log_level level for server logging
    :param log_modules parent modules under which logging can be observed
    :param handler: SpecialHandler class or another class derived from SpecialHandler
    :param handler_args: arguments to be passed to the handler class
    :param handler_type: variable used for instantiating simple server - either `socket` or anything else
    :param backend: function: takes server as argument and loops continuously allowing for other stateful operations
    :param backend_init: function: takes server as argument and initializes backend
    :param backend_shutdown: function: takes server as argument and shuts down any backend activity
    :param interval: length of rate limit interval (seconds)
    :param req_per_interval: number of requests allowed in given interval
    :param blacklist: number of requests above rate limit to blacklist an ip
    """
    _setup_log(log_level, log_modules)
    if not handler_args:
        if isinstance(handler, SocketHandler):
            pass
        elif handler_type == 'socket':
            handler_args = ({'/':  partial(socket_response, basic_socket_generator)},)
        else:
            handler_args = ({'/': basic_handler},)
    h = handler(*handler_args, interval=interval, req_per_interval=req_per_interval, blacklist=blacklist)
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(_async_serve(address, backend, backend_init, backend_shutdown, h, loop))
    except KeyboardInterrupt:
        loop.close()
