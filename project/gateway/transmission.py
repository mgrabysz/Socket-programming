import json
import socket
import time
from typing import Any

import authorization
import registration

_registered_devices = set()
_package = dict()


def _update_registered_devices():
    global _registered_devices
    _registered_devices = registration.get_registered_devices()


def _reset_package():
    global _package
    _package = dict()
    _package["devices"] = dict()
    for device in _registered_devices:
        _package["devices"][device] = None


def _get_package() -> dict:
    global _package
    if "devices" not in _package.keys():
        _package["devices"] = dict()
    _package["timestamp"] = time.time()
    return _package


def _add_payload_to_package(device_id: int, payload: Any):
    global _package
    _package["devices"][device_id] = payload


def handle_message(message: dict):
    print(f"handling transmission message: {message}")

    if (
        "device_id" not in message
        or "timestamp" not in message
        or "payload" not in message
    ):
        print("Incomplete transmission")
        return

    if message["device_id"] not in _registered_devices:
        print(f"Invalid device id, device is not registered")
        print(_registered_devices)
        return

    _add_payload_to_package(message["device_id"], message["payload"])


def transmit(servers: list[tuple[str, int]], interval: float, ac: authorization.AuthorizationCenter, verbose: bool):
    udp_client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    while True:
        msg_to_send = _get_package()
        msg_bytes = json.dumps(msg_to_send).encode()
        signature = ac.signature(msg_bytes)
        print("Message send to servers:")
        if verbose:
            print(f"Signature: {signature}")
        else:
            print(f"Signature: {signature[0:10]}...")
        print(f"Payload: {msg_to_send}")
        _update_registered_devices()
        _reset_package()

        for server in servers:
            bytes_sent = udp_client_socket.sendto(signature + msg_bytes, server)
            print(f"{bytes_sent} bytes send to server {server[0]}:{server[1]}")

        print("")
        time.sleep(interval)
