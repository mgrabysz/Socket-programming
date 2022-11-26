import socket
import argparse


BUF_SIZE = 64
HOST_IP = '127.0.0.1'


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("port")
    return parser


if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()

    server_address_port = (HOST_IP, int(args.port))

    udp_server_socket = socket.socket(
        family=socket.AF_INET, type=socket.SOCK_DGRAM)
    udp_server_socket.bind(server_address_port)

    print(
        f'UDP server up and listening on host {server_address_port[0]}, ' +
        f'port {server_address_port[1]}')

    while(True):

        message_address = udp_server_socket.recvfrom(BUF_SIZE)
        message = message_address[0]
        address = message_address[1]

        if not message:
            print("Error in datagram")
            break

        print(f'Client IP Address: {address}')
        print(f'Client message: {message.decode("utf-8")}')
