import random
import socket
import time
import argparse
from threading import Lock, Thread

from messages import Register_message, Transmission_message, Unregister_message

# defaults
SERVER_IP = '127.0.0.1'
SERVER_PORT = 2137
NUM_OF_DEVICES = 5  # number of devices (threads) to be launched
NUM_OF_MESSAGES = 5  # number of messages per thread to send
INTERVAL = 3  # interval between messages in seconds


class Client:
    def __init__(self, device_id, server_ip, server_port, client_socket, lock):
        self.socket = client_socket
        self.lock = lock
        self.device_id = device_id
        self.server_address = (server_ip, server_port)

    def transmit(self, num_of_messages, interval):
        """
        :param num_of_messages: number of messages to be sent
        :param interval: interval in seconds
        """
        self.send_register_message()

        for _ in range(num_of_messages):
            time.sleep(interval)
            payload = random.random()
            self.send_transmission_message(payload)

        self.send_unregister_message()

    def send_register_message(self):
        register_message = Register_message(self.device_id, time.time())
        msg_bytes = register_message.to_json().encode()
        self.socket.sendto(msg_bytes, self.server_address)
        with self.lock:
            print(f'Sent register message from device {self.device_id}')

    def send_unregister_message(self):
        unregister_message = Unregister_message(self.device_id)
        msg_bytes = unregister_message.to_json().encode()
        self.socket.sendto(msg_bytes, self.server_address)
        with self.lock:
            print(f'Sent unregister message from device {self.device_id}')

    def send_transmission_message(self, payload):
        register_message = Transmission_message(self.device_id, time.time(), payload)
        msg_bytes = register_message.to_json().encode()
        self.socket.sendto(msg_bytes, self.server_address)
        with self.lock:
            print(f'Message sent: {payload} from device {self.device_id}')


class Client_manager():
    def __init__(self, client_socket, server_ip, server_port, num_of_devices, num_of_messages, interval, first_id):
        self.num_of_devices = num_of_devices
        self.interval = interval
        self.num_of_messages = num_of_messages
        self.server_port = server_port
        self.server_ip = server_ip
        self.client_socket = client_socket
        self.lock = Lock()
        self.threads = []
        self.first_id = first_id

    def run_devices(self):

        for i in range(self.num_of_devices):
            self.threads.append(Thread(target=multi_threaded_client, args=(
                self.first_id + i, self.server_ip, self.server_port,
                self.num_of_messages, self.interval, self.client_socket, self.lock
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


def multi_threaded_client(device_id, server_ip, server_port, num_of_messages, interval, client_socket, lock):
    client = Client(device_id, server_ip, server_port, client_socket, lock)
    client.transmit(num_of_messages, interval)


if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()

    client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    client_manager = Client_manager(
        client_socket=client_socket,
        server_ip=args.address,
        server_port=int(args.port),
        num_of_devices=int(args.devices),
        num_of_messages=int(args.messages),
        interval=int(args.interval),
        first_id=int(args.id)
    )
    client_manager.run_devices()
