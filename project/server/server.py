import socket
import json
from threading import Lock, Thread

BUF_SIZE = 65536
HOST_IP = ""
PORTS = list(range(2140, 2142))
NUM_OF_DEVICES = 1


class Server:
    def __init__(self, device_id, host_ip, port, lock):
        self.device_id = device_id
        self.host_ip = host_ip
        self.port = port
        self.lock = lock

        self.server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

        self.server_socket.bind((self.host_ip, self.port))

        print(f'Server nr {self.device_id} up and listening on port {self.port}')

    def listen(self):
        message_bytes = self.server_socket.recv(BUF_SIZE)
        message_json = json.loads(message_bytes)

        print(f'Server nr {self.device_id} received message: {message_json}')


class ServerManager:
    def __init__(self, ports, host_ip, num_of_devices):
        self.ports = ports
        self.host_ip = host_ip
        self.num_of_devices = num_of_devices
        self.lock = Lock()
        self.threads = []

    def run_devices(self):
        for device_nr, port in zip(range(self.num_of_devices), self.ports):
            self.threads.append(Thread(target=multi_threaded_server, args=(
                device_nr, port, self.host_ip, self.lock
            )))

        for thread in self.threads:
            thread.start()

        for thread in self.threads:
            thread.join()


def multi_threaded_server(device_id, port, host_ip, lock):
    server = Server(device_id, host_ip, port, lock)

    while True:
        server.listen()


def main():
    server_manager = ServerManager(PORTS, HOST_IP, NUM_OF_DEVICES)
    server_manager.run_devices()


if __name__ == "__main__":
    main()
