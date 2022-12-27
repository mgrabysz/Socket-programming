import random
import socket
import time

from messages import Register_message, Transmission_message, Unregister_message

SERVER_IP = '127.0.0.1'
SERVER_PORT = 2137
class Client:
    def __init__(self, device_id, server_ip, server_port):
        self.device_id = device_id
        self.server_address = (server_ip, server_port)

    def transmit(self, num_of_messages, interval=3):
        """
        :param num_of_messages: number of messages to be sent
        :param interval: interval in seconds
        :return:
        """
        client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        bytes_sent = self.send_register_message(client_socket)
        print(f'Bytes sent (register message): {bytes_sent}')

        for _ in range(num_of_messages):
            time.sleep(interval)
            payload = random.random()
            bytes_sent = self.send_transmission_message(client_socket, payload)
            print(f'Message sent: {payload}')
            print(f'Bytes sent: {bytes_sent}')

        bytes_sent = self.send_unregister_message(client_socket)
        print(f'Bytes sent (unregister message): {bytes_sent}')

    def send_register_message(self, client_socket):
        register_message = Register_message(self.device_id, time.time())
        msg_bytes = register_message.to_json().encode()
        return client_socket.sendto(msg_bytes, self.server_address)

    def send_unregister_message(self, client_socket):
        unregister_message = Unregister_message(self.device_id)
        msg_bytes = unregister_message.to_json().encode()
        return client_socket.sendto(msg_bytes, self.server_address)

    def send_transmission_message(self, client_socket, payload):
        register_message = Transmission_message(self.device_id, time.time(), payload)
        msg_bytes = register_message.to_json().encode()
        return client_socket.sendto(msg_bytes, self.server_address)


if __name__ == "__main__":

    client = Client(1, SERVER_IP, SERVER_PORT)
    client.transmit(10)