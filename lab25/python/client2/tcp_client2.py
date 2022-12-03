import socket
import argparse
import time

MESSAGE = "This is our message - POLSKA WYSZŁA Z GRUPY NA MUNDIALU kochamy cię Szczęsny"


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("ip_address")
    parser.add_argument("port")
    return parser


if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()
    server_address_port = (args.ip_address, int(args.port))

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(server_address_port)
        messages = MESSAGE.split(" ")
        for message in messages:
            message += " "
            s.sendall(bytes(message, "UTF-8"))
            print(f"Message sent: {message}")
            time.sleep(1)
