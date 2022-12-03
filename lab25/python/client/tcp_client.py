import socket
import argparse
import time


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

        for countdown in reversed(range(10)):
            s.sendall(bytes(str(countdown), "UTF-8"))
            print(f"Message sent {countdown}")
            time.sleep(1)
