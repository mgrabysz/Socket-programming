import time
import socket
import json
from typing import List, Any
import registration
import authorization

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
    if "devices" not in __package.keys():
        __package["devices"] = dict()
    __package["timestamp"] = time.time()
    return __package


def __add_payload_to_package(device_id: int, payload: Any):
    global __package
    __package["devices"][device_id] = payload


def handle_message(message: dict):
    print(f"handling transmission message: {message}")

    if (
        "device_id" not in message
        or "timestamp" not in message
        or "payload" not in message
    ):
        print("Incomplete transmission")
        return

    if message["device_id"] not in __registered_devices:
        print(f"Invalid device id, device is not registered")
        print(__registered_devices)
        return

    __add_payload_to_package(message["device_id"], message["payload"])


def transmit(address: str, ports: List[int], interval: float, ac: authorization.AuthorizationCenter, verbose: bool):
    udp_client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    while True:
        msg_to_send = __get_package()
        msg_bytes = json.dumps(msg_to_send).encode()
        signature = ac.signature(msg_bytes)
        msg_to_send["signature"] = signature.decode('unicode_escape')
        msg_bytes = json.dumps(msg_to_send, ensure_ascii=False).encode('utf-8')

        if not verbose:
            msg_to_send["signature"] = msg_to_send["signature"][0:10] + "..."
        print(f"Message send to servers:\n{msg_to_send}")
        __update_registered_devices()
        __reset_package()

        for port in ports:
            server_address_port = (address, int(port))
            bytes_sent = udp_client_socket.sendto(msg_bytes, server_address_port)
            print(f"{bytes_sent} bytes send to server running on port: {port}")

        time.sleep(interval)
