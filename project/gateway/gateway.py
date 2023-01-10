import argparse
import json
import socket
from threading import Thread

import registration
import transmission
import authorization

SERVER_IP = ''
GATEWAY_PORT = 2137
SERVER_PORTS = [2140, 2141]
INTERVAL = 3


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", default=GATEWAY_PORT, help="port of the server")
    parser.add_argument("-a", "--address", default=SERVER_IP, help="ip address of the server")
    parser.add_argument("-i", "--interval", default=INTERVAL, help="interval between messages in seconds")
    parser.add_argument("-k", "--key", help="path to the private key in .pem format")
    parser.add_argument("-v", "--verbose", action="store_true")
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    server_address_port = (args.address, int(args.port))
    udp_server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    udp_server_socket.bind(server_address_port)
    print(f'Gateway listening on port {args.port}')

    authorization_center = authorization.AuthorizationCenter(path=args.key)

    thread = Thread(target=transmission.transmit,
                    args=(args.address, SERVER_PORTS, int(args.interval), authorization_center, args.verbose))
    thread.start()

    while True:
        message_bytes = udp_server_socket.recv(65536)
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
