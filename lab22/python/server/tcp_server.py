import socket
import argparse

HOST_IP = ""
BUF_SIZE = 6


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("port")
    return parser


def work():
    return True


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
            with conn:
                print(f'Listening from host {addr[0]}, on port {addr[1]}')
                full_message = ""
                while True:
                    partial_message = conn.recv(BUF_SIZE)
                    if not partial_message:
                        break
                    print(f'Received {len(partial_message)} bytes')
                    full_message += partial_message.decode("utf-8")

                print(f'Full client message: {full_message}')
