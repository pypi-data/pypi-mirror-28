import argparse

from . import serve

parser = argparse.ArgumentParser(description='Run basic aioserverplus Server')
parser.add_argument('--port', metavar='p', type=int, default=9999,
                    help='port number')
parser.add_argument('--address', metavar='a', type=str, default='localhost',
                    help='ip address')
parser.add_argument('--log-level', metavar='lvl', type=str, default='INFO',
                    help='logging level for server to stdout')
parser.add_argument('--interval', metavar='int', type=float, default=0.,
                    help='rate limit interval')
parser.add_argument('--requests-per-interval', metavar='rpi', type=float, default=0.,
                    help='number of requests allowed in rate limit interval')
parser.add_argument('--requests-to-blacklist', metavar='rtb', type=float, default=0.,
                    help='number of requests over rate limit in interval to blacklist ip')
parser.add_argument('--type', metavar='t', type=str, default='regular',
                    help='Type of server to host (regular, socket)')
args = parser.parse_args()
print('Now serving on http://{}:{}'.format(args.address, args.port))
serve(address=(args.address, args.port), log_level=args.log_level, handler_type=args.type,
      interval=args.interval, req_per_interval=args.requests_per_interval, blacklist=args.requests_to_blacklist)
