import time
import socket
import json

import registration

__registered_devices = set()
__package = dict()


def __update_registered_devices():
    global __registered_devices
    __registered_devices = registration.get_registered_devices()


def __reset_package():
    global __package
    __package = dict()
    __package["devices"] = dict()
    for device in __registered_devices:
        __package["devices"][device] = None


def __get_package() -> dict:
    global __package
    __package["timestamp"] = time.time()
    return __package


def __add_payload_to_package(device_id: int, payload):
    global __package
    __package["devices"][device_id] = payload


def handle_message(message: dict):
    print(f"handling transmission message: {message}")

    if "device_id" not in message or "timestamp" not in message or "payload" not in message:
        print("Incomplete transmmition")
        return

    if message["device_id"] not in __registered_devices:
        print(f"Invalid device id, device is not registered")
        return

    __add_payload_to_package(message["device_id"], message["payload"])


def transmit(ports, interval):
    udp_client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    while True:
        msg_bytes = json.dumps(__get_package()).encode()
        __update_registered_devices()
        __reset_package()

        for port in ports:
            bytes_sent = udp_client_socket.sendto(msg_bytes, port)
            print(f"Bytes send: {bytes_sent}, to server running on port: {port}")

        time.sleep(interval)
