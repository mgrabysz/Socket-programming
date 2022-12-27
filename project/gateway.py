import argparse
import json
import socket

import registration
import transmission


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("port")
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    server_address_port = ('', int(args.port))
    udp_server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    udp_server_socket.bind(server_address_port)
    print(f'Gateway listening on port {args.port}')

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
