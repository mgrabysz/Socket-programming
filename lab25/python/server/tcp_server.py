import socket
import argparse
import threading
from _thread import *

HOST_IP = ""
BUF_SIZE = 64


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("port")
    return parser


def work():
    return True


def multi_threaded_client(connection):
    while work():
        message = connection.recv(BUF_SIZE)
        if not message:
            break
        print(f'Thread id: {threading.get_native_id()}, received message: {message.decode("utf-8")}')
    connection.close()


if __name__ == "__main__":

    parser = create_parser()
    args = parser.parse_args()
    server_address_port = (HOST_IP, int(args.port))

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(server_address_port)
        s.listen()
        print(f'TCP server up and listening on port {server_address_port[1]}')

        while work():
            conn, addr = s.accept()
            print(f'Connected to client from host {addr[0]}, on port {addr[1]}')
            start_new_thread(multi_threaded_client, (conn, ))
