"""
Projekt PSI - System agregacji dokumentów
Autorzy: Marcin Grabysz
Data utworzenia: 27.12.2022
"""

import argparse
import json
import random
import socket
import time
from threading import Lock, Thread

from messages import (RegisterMessage, TransmissionMessage,
                      UnregisterMessage, SyncMessage)

# defaults
SERVER_IP = '127.0.0.1'
SERVER_PORT = 2137
NUM_OF_DEVICES = 5  # number of devices (threads) to be launched
NUM_OF_MESSAGES = 5  # number of messages per thread to send
INTERVAL = 10  # interval between messages in seconds
BUF_SIZE = 65536  # size (bytes) of buffer used to receive sync messages
JITTER = 0.1


class Client:
    def __init__(self,
                 device_id: int,
                 server_ip: str,
                 server_port: int,
                 lock: Lock,
                 interval: float,
                 random_start: bool,
                 initial_jitter: float) -> None:
        self.socket = socket.socket(family=socket.AF_INET,
                                    type=socket.SOCK_DGRAM)
        self.lock = lock
        self.device_id = device_id
        self.server_address = (server_ip, server_port)
        self.interval = interval
        self.jitter = initial_jitter
        self.reference_time = time.time()

        if random_start:
            self.reference_time += self.interval * random.random()

        Thread(target=self.listen_for_sync_messages, args=()).start()

    def next_transmit(self) -> tuple[int, float]:
        jitter_seconds = self.jitter * self.interval
        seconds_since_reference = time.time() - self.reference_time
        next_transmit_index = int(
            (seconds_since_reference + jitter_seconds) // self.interval + 1)
        next_transmit_time = (
            self.reference_time + next_transmit_index * self.interval)
        return next_transmit_index, next_transmit_time

    def listen_for_sync_messages(self) -> None:
        while True:
            message_bytes = self.socket.recv(BUF_SIZE)
            message_json = json.loads(message_bytes)
            message = SyncMessage.from_json(message_json)
            self.reference_time = message.reference_time
            self.jitter = message.jitter
            print(f'Received sync message, reference {self.reference_time}' +
                  f' jitter {self.jitter}')

    def transmit(self, num_of_messages: int) -> None:
        """
        :param num_of_messages: number of messages to be sent
        """
        self.send_register_message()

        for _ in range(num_of_messages):
            random_offset = random.uniform(-self.jitter, self.jitter) * self.interval
            next_transmit_index, next_transmit_time = self.next_transmit()
            time.sleep(next_transmit_time - time.time() + random_offset)

            payload = random.random()
            self.send_transmission_message(next_transmit_index, payload)

        self.send_unregister_message()

    def send_register_message(self) -> None:
        register_message = RegisterMessage(self.device_id, time.time())
        msg_bytes = register_message.to_json().encode()
        self.socket.sendto(msg_bytes, self.server_address)
        with self.lock:
            print(f'Sent register message from device {self.device_id}')

    def send_unregister_message(self) -> None:
        unregister_message = UnregisterMessage(self.device_id)
        msg_bytes = unregister_message.to_json().encode()
        self.socket.sendto(msg_bytes, self.server_address)
        with self.lock:
            print(f'Sent unregister message from device {self.device_id}')

    def send_transmission_message(self, i: int, payload: float) -> None:
        register_message = TransmissionMessage(self.device_id, time.time(), payload)
        msg_bytes = register_message.to_json().encode()
        self.socket.sendto(msg_bytes, self.server_address)
        with self.lock:
            print(f'Message {i} sent: {payload} from device {self.device_id}')


class ClientManager:
    def __init__(self,
                 server_ip: str,
                 server_port: int,
                 num_of_devices: int,
                 num_of_messages: int,
                 interval: float,
                 first_id: int,
                 random_start: bool,
                 initial_jitter: float):
        self.num_of_devices = num_of_devices
        self.interval = interval
        self.num_of_messages = num_of_messages
        self.server_port = server_port
        self.server_ip = server_ip
        self.lock = Lock()
        self.threads = []
        self.first_id = first_id
        self.random_start = random_start
        self.initial_jitter = initial_jitter

    def run_devices(self) -> None:

        for i in range(self.num_of_devices):
            self.threads.append(Thread(target=multi_threaded_client, args=(
                self.first_id + i, self.server_ip, self.server_port,
                self.num_of_messages, self.interval, self.lock,
                self.random_start, self.initial_jitter
            )))

        for thread in self.threads:
            thread.start()

        for thread in self.threads:
            thread.join()


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--address", default=SERVER_IP,
                        help="ip address of the server")
    parser.add_argument("-p", "--port", default=SERVER_PORT,
                        help="port of the server")
    parser.add_argument("-d", "--devices", default=NUM_OF_DEVICES,
                        help="number of devices (threads) to be launched")
    parser.add_argument("-m", "--messages", default=NUM_OF_MESSAGES,
                        help="number of messages to be sent from device")
    parser.add_argument("-i", "--interval", default=INTERVAL,
                        help="interval between messages in seconds")
    parser.add_argument("--random_start", action="store_true",
                        help="add random delay before first transmission")
    parser.add_argument("--initial_jitter", type=float, default=JITTER,
                        help="jitter value to use before first synchronization")
    parser.add_argument("--id", default=0, help="id of the first device created")
    return parser


def multi_threaded_client(device_id: int, server_ip: str, server_port: int,
                          num_of_messages: int, interval: float, lock: Lock,
                          random_start: bool, initial_jitter: float) -> None:
    client = Client(device_id, server_ip, server_port, lock, interval,
                    random_start, initial_jitter)
    client.transmit(num_of_messages)


def main():
    parser = create_parser()
    args = parser.parse_args()

    client_manager = ClientManager(
        server_ip=args.address,
        server_port=int(args.port),
        num_of_devices=int(args.devices),
        num_of_messages=int(args.messages),
        interval=float(args.interval),
        first_id=int(args.id),
        initial_jitter=float(args.initial_jitter),
        random_start=args.random_start
    )
    client_manager.run_devices()


if __name__ == "__main__":
    main()
