"""
Projekt PSI - System agregacji dokumentów
Autorzy: Patrycja Wysocka
Data utworzenia: 29.12.2022
"""

import json
import socket
import argparse
from threading import Lock, Thread

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding

BUF_SIZE = 65536
HOST_IP = ""
DEAFULT_SERVER_PORTS = list(range(2140, 2142))
NUM_OF_DEVICES = 2
DEFAULT_PUBLIC_KEY_PATH = "pubkey.pem"


class Server:
    def __init__(self, device_id: int, host_ip: int, port: int,
                 lock: Lock, public_key_path: str) -> None:
        self.device_id = device_id
        self.host_ip = host_ip
        self.port = port
        self.lock = lock

        self.server_socket = socket.socket(family=socket.AF_INET,
                                           type=socket.SOCK_DGRAM)

        self.server_socket.bind((self.host_ip, self.port))

        print(f'Server nr {self.device_id} up and listening on port {self.port}')

        with open(public_key_path, "rb") as f:
            self.public_key = serialization.load_pem_public_key(f.read())

    def listen(self) -> None:
        message_bytes = self.server_socket.recv(BUF_SIZE)

        signature, payload_bytes = message_bytes[:256], message_bytes[256:]

        try:
            self.public_key.verify(
                signature,
                payload_bytes,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
        except InvalidSignature:
            print("Signature verification failed")
            return

        payload_json = json.loads(payload_bytes)
        print(f'Server nr {self.device_id} ' +
              f'received verified message: {payload_json}')


class ServerManager:
    def __init__(self, ports: int, host_ip: int,
                 num_of_devices: int, public_key_path: str) -> None:
        self.ports = ports
        self.host_ip = host_ip
        self.num_of_devices = num_of_devices
        self.lock = Lock()
        self.threads = []
        self.public_key_path = public_key_path

    def run_devices(self):
        for device_nr, port in zip(range(self.num_of_devices), self.ports):
            self.threads.append(Thread(target=multi_threaded_server, args=(
                device_nr, port, self.host_ip, self.lock, self.public_key_path
            )))

        for thread in self.threads:
            thread.start()

        for thread in self.threads:
            thread.join()


def multi_threaded_server(device_id, port, host_ip, lock, public_key_path):
    server = Server(device_id, host_ip, port, lock, public_key_path)

    while True:
        server.listen()


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", dest="server_ports",
                        action="append", help="server port")
    parser.add_argument("-pk", "--public_key", default=DEFAULT_PUBLIC_KEY_PATH,
                        help="path to the public key in .pem format")
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()
    if not args.server_ports:
        servers_ports = DEAFULT_SERVER_PORTS
        num_of_devices = NUM_OF_DEVICES
    else:
        servers_ports = [int(port) for port in args.server_ports]
        num_of_devices = len(servers_ports)
        if num_of_devices > 32:
            raise Exception("Number of servers can't be greater than 32!")

    server_manager = ServerManager(servers_ports, HOST_IP,
                                   num_of_devices, args.public_key)
    server_manager.run_devices()


if __name__ == "__main__":
    main()
