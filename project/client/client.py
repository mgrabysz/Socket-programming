import argparse
import json
import random
import socket
import time
from threading import Lock, Thread

from messages import RegisterMessage, TransmissionMessage, UnregisterMessage

# defaults
SERVER_IP = '127.0.0.1'
SERVER_PORT = 2137
NUM_OF_DEVICES = 5  # number of devices (threads) to be launched
NUM_OF_MESSAGES = 5  # number of messages per thread to send
INTERVAL = 10  # interval between messages in seconds
BUF_SIZE = 65536  # size (bytes) of buffer used to receive sync messages
JITTER = 0.1


class Client:
    def __init__(self, device_id, server_ip, server_port, lock, interval):
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.lock = lock
        self.device_id = device_id
        self.server_address = (server_ip, server_port)
        self.interval = interval
        self.reference_time = time.time() - random.random() * interval
        self.jitter = JITTER

        Thread(target=self.listen_for_sync_messages, args=()).start()

    def next_transmit_time(self) -> float:
        elapsed = time.time() - self.reference_time
        completed_transmissions = elapsed // self.interval
        return self.reference_time + completed_transmissions * self.interval + self.interval

    def listen_for_sync_messages(self):
        while True:
            message_bytes = self.socket.recv(BUF_SIZE)
            message_json = json.loads(message_bytes)
            print("Received sync message")
            self.reference_time = message_json["reference_time"]
            self.jitter = message_json["jitter"]

    def transmit(self, num_of_messages):
        """
        :param num_of_messages: number of messages to be sent
        """
        self.send_register_message()
        # @TODO hangle JITTER
        for _ in range(num_of_messages):
            time.sleep(self.next_transmit_time() - time.time())

            payload = random.random()
            self.send_transmission_message(payload)

        self.send_unregister_message()

    def send_register_message(self):
        register_message = RegisterMessage(self.device_id, time.time())
        msg_bytes = register_message.to_json().encode()
        self.socket.sendto(msg_bytes, self.server_address)
        with self.lock:
            print(f'Sent register message from device {self.device_id}')

    def send_unregister_message(self):
        unregister_message = UnregisterMessage(self.device_id)
        msg_bytes = unregister_message.to_json().encode()
        self.socket.sendto(msg_bytes, self.server_address)
        with self.lock:
            print(f'Sent unregister message from device {self.device_id}')

    def send_transmission_message(self, payload):
        register_message = TransmissionMessage(self.device_id, time.time(), payload)
        msg_bytes = register_message.to_json().encode()
        self.socket.sendto(msg_bytes, self.server_address)
        with self.lock:
            print(f'Message sent: {payload} from device {self.device_id}')


class ClientManager:
    def __init__(self, server_ip, server_port, num_of_devices, num_of_messages, interval, first_id):
        self.num_of_devices = num_of_devices
        self.interval = interval
        self.num_of_messages = num_of_messages
        self.server_port = server_port
        self.server_ip = server_ip
        self.lock = Lock()
        self.threads = []
        self.first_id = first_id

    def run_devices(self):

        for i in range(self.num_of_devices):
            self.threads.append(Thread(target=multi_threaded_client, args=(
                self.first_id + i, self.server_ip, self.server_port,
                self.num_of_messages, self.interval, self.lock
            )))

        for thread in self.threads:
            thread.start()

        for thread in self.threads:
            thread.join()


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--address", default=SERVER_IP, help="ip address of the server")
    parser.add_argument("-p", "--port", default=SERVER_PORT, help="port of the server")
    parser.add_argument("-d", "--devices", default=NUM_OF_DEVICES, help="number of devices (threads) to be launched")
    parser.add_argument("-m", "--messages", default=NUM_OF_MESSAGES, help="number of messages to be sent from device")
    parser.add_argument("-i", "--interval", default=INTERVAL, help="interval between messages in seconds")
    parser.add_argument("--id", default=0, help="id of the first device created")
    return parser


def multi_threaded_client(device_id, server_ip, server_port, num_of_messages, interval, lock):
    client = Client(device_id, server_ip, server_port, lock, interval)
    client.transmit(num_of_messages)


def main():
    parser = create_parser()
    args = parser.parse_args()

    client_manager = ClientManager(
        server_ip=args.address,
        server_port=int(args.port),
        num_of_devices=int(args.devices),
        num_of_messages=int(args.messages),
        interval=int(args.interval),
        first_id=int(args.id)
    )
    client_manager.run_devices()


if __name__ == "__main__":
    main()
