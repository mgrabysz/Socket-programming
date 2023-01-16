import json
import time
import socket

import registration


def next_sync_time(interval: float, reference_time: float) -> float:
    elapsed = time.time() - reference_time
    completed_transmissions = elapsed // interval
    return reference_time + completed_transmissions * interval + interval


def send_sync_messages(interval: float, reference_time: float):
    sync_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    while True:
        time.sleep(next_sync_time(interval, reference_time) - time.time())

        payload = json.dumps({"reference_time": reference_time}).encode('utf-8')
        for address in registration.get_registered_devices().values():
            print(f"Sending sync message to {address}")
            sync_socket.sendto(payload, address)
