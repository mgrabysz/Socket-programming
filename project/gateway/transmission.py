import json
import socket
import time
from typing import Any, Dict

import authentication
import registration
import logging

logging.basicConfig(filename='./gateway.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger(__name__)

_registered_devices: Dict[int, registration.Address] = {}
_package = dict()


def _update_registered_devices() -> None:
    global _registered_devices
    _registered_devices = registration.get_registered_devices()


def _reset_package() -> None:
    global _package
    _package = dict()
    _package["devices"] = dict()
    for device_id in _registered_devices.keys():
        _package["devices"][device_id] = []


def _check_registered_devices() -> None:
    global _package
    unused_devices = []
    for device in _package["devices"].keys():
        if len(_package["devices"][device]) == 0:
            _package["devices"][device] = None
            unused_devices.append(device)
    if len(unused_devices) != 0:
        msg = f"Registered devices that did not send any transmission data: {unused_devices}"
        print(msg)
        logger.info(msg)


def _get_package() -> dict:
    global _package
    if "devices" not in _package.keys():
        _package["devices"] = dict()
    _package["timestamp"] = time.time()
    _check_registered_devices()
    return _package


def _add_payload_to_package(device_id: int, payload: Any) -> None:
    global _package
    if device_id not in _package["devices"].keys():
        _package["devices"][device_id] = []
    _package["devices"][device_id].append(payload)


def handle_message(message: dict) -> None:
    print(f"handling transmission message: {message}")

    if (
            "device_id" not in message
            or "timestamp" not in message
            or "payload" not in message
    ):
        msg = "Incomplete transmission"
        print(msg)
        logger.warning(msg)
        return

    if message["device_id"] not in _registered_devices.keys():
        msg = f"Invalid device id={message['device_id']}, device is not registered!"
        print(msg)
        logger.warning(msg)
        return

    _add_payload_to_package(message["device_id"], message["payload"])


def transmit(
        servers: list[tuple[str, int]],
        interval: float,
        ac: authentication.AuthenticationCenter,
        verbose: bool,
        reference_time: float
) -> None:
    udp_client_socket = socket.socket(family=socket.AF_INET,
                                      type=socket.SOCK_DGRAM)

    while True:
        msg_to_send = _get_package()
        msg_bytes = json.dumps(msg_to_send).encode()
        signature = ac.signature(msg_bytes)
        print("Message send to servers:")
        if verbose:
            print(f"Signature: {signature.hex()}")
        else:
            print(f"Signature: {signature[:10].hex()}...")
        print(f"Payload: {msg_to_send}")
        _update_registered_devices()
        _reset_package()

        for server in servers:
            bytes_sent = udp_client_socket.sendto(
                signature + msg_bytes, server)
            print(f"{bytes_sent} bytes send to server {server[0]}: {server[1]}")

        print("")
        time.sleep(interval)
