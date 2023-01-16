import argparse
import json
import socket
import time
from threading import Thread

import registration
import authentication
import sync
import transmission

DEFAULT_GATEWAY_PORT = 2137
DEFAULT_SERVERS = [("127.0.0.1", 2140), ("127.0.0.1", 2141)]
DEFAULT_INTERVAL = 3
DEFAULT_SYNC_INTERVAL = 10
DEFAULT_PRIVATE_KEY_PATH = "./privkey.pem"
DEFAULT_PUBLIC_KEY_PATH = "../server/pubkey.pem"
DEFAULT_KEY_PASSWORD = "Qwerty123"


class Gateway:
    def __init__(self, port: int, servers, interval: float, sync_interval: float, private_key, public_key, key_password,
                 is_verbose):
        self.port = port
        self.servers = servers
        self.interval = interval
        self.sync_interval = sync_interval
        self.private_key = private_key
        self.public_key = public_key
        self.key_password = key_password
        self.is_verbose = is_verbose
        self.reference_time = time.time()

    def start(self):
        listen_port = ('', self.port)
        listen_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        listen_socket.bind(listen_port)
        print(f'Gateway listening on port {self.port}')

        authentication_center = authentication.AuthenticationCenter(self.private_key, self.public_key,
                                                                    self.key_password)

        # start a thread for getting data from clients and sending it to servers
        Thread(
            target=transmission.transmit,
            args=(self.servers, self.interval, authentication_center, self.is_verbose, self.reference_time)
        ).start()

        # start a thread for sending sync messages to clients
        Thread(
            target=sync.send_sync_messages,
            args=(self.sync_interval, self.reference_time)
        ).start()

        while True:
            message_bytes, address = listen_socket.recvfrom(65536)
            message_json = json.loads(message_bytes)
            print(f'Received message: {message_json}')

            if 'action' not in message_json:
                print('No action field in message')
                return

            action = message_json['action']
            if action in {'register', 'unregister'}:
                registration.handle_message(address, message_json)
            elif action == 'transmit':
                transmission.handle_message(message_json)
            else:
                print(f'Invalid action {action}')


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", default=DEFAULT_GATEWAY_PORT, help="port of the gateway")
    parser.add_argument("-s", "--server", dest="server_strs", action="append", help="ip:port of a server")
    parser.add_argument("-i", "--interval", default=DEFAULT_INTERVAL, help="interval between messages in seconds")
    parser.add_argument("--sync_interval", default=DEFAULT_SYNC_INTERVAL,
                        help="interval between time synchronization messages in seconds")
    parser.add_argument("--private_key", default=DEFAULT_PRIVATE_KEY_PATH,
                        help="path to the private key in .pem format")
    parser.add_argument("--public_key", default=DEFAULT_PUBLIC_KEY_PATH, help="path to the public key in .pem format")
    parser.add_argument("--key_password", default=DEFAULT_KEY_PASSWORD, help="password to the private key")
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

    gateway = Gateway(
        port=int(args.port),
        servers=servers,
        interval=int(args.interval),
        sync_interval=int(args.sync_interval),
        private_key=args.private_key,
        public_key=args.public_key,
        key_password=args.key_password,
        is_verbose=args.verbose
    )
    gateway.start()


if __name__ == "__main__":
    main()
