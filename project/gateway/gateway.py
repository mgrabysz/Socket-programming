import argparse
import json
import socket
from threading import Thread

import registration
import transmission
import authorization

DEFAULT_GATEWAY_PORT = 2137
DEFAULT_SERVERS = [("127.0.0.1", 2140), ("127.0.0.1", 2141)]
DEFAULT_INTERVAL = 3


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", default=DEFAULT_GATEWAY_PORT, help="port of the gateway")
    parser.add_argument("-s", "--server", dest="server_strs", action="append", help="ip:port of a server")
    parser.add_argument("-i", "--interval", default=DEFAULT_INTERVAL, help="interval between messages in seconds")
    parser.add_argument("-k", "--key", help="path to the private key in .pem format")
    parser.add_argument("-v", "--verbose", action="store_true")
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()
    print(args.server_strs)
    if not args.server_strs:
        servers = DEFAULT_SERVERS
    else:
        servers = [(server_str.split(':')[0], int(server_str.split(':')[1])) for server_str in args.server_strs]

    listen_port = ('', int(args.port))
    listen_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    listen_socket.bind(listen_port)
    print(f'Gateway listening on port {args.port}')

    authorization_center = authorization.AuthorizationCenter(path=args.key)

    thread = Thread(target=transmission.transmit,
                    args=(servers, int(args.interval), authorization_center, args.verbose))
    thread.start()

    while True:
        message_bytes = listen_socket.recv(65536)
        message_json = json.loads(message_bytes)

        print(f'Received message: {message_json}')

        if 'action' not in message_json:
            print('No action field in message')
            return

        action = message_json['action']
        if action in {'register', 'unregister'}:
            registration.handle_message(message_json)
        elif action == 'transmit':
            transmission.handle_message(message_json)
        else:
            print(f'Invalid action {action}')


if __name__ == "__main__":
    main()
