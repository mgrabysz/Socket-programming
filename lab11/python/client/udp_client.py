import socket
import argparse


BUF_SIZE = 1


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("ip_address")
    parser.add_argument("port")
    return parser


if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()

    server_address_port = (args.ip_address, int(args.port))

    # Create a UDP socket at client side
    udp_client_socket = socket.socket(
        family=socket.AF_INET, type=socket.SOCK_DGRAM)

    for countdown in reversed(range(10)):
        msg_bytes = str(countdown).encode()
        bytes_sent = udp_client_socket.sendto(msg_bytes, server_address_port)

        print(f'Bytes sent: {bytes_sent}')
