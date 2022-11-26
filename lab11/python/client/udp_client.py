import socket
import argparse


BUF_SIZE = 64


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

    for countdown in reversed(range(11)):
        msg = "BOOM!" if countdown == 0 else str(countdown)
        msg_bytes = str.encode(msg)
        bytes_send = udp_client_socket.sendto(msg_bytes, server_address_port)

        print(f'Bytes send: {bytes_send}')
