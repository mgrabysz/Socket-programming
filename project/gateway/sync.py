import json
import time
import socket

import registration


def next_sync_time(interval: float, reference_time: float) -> float:
    elapsed = time.time() - reference_time
    completed_transmissions = elapsed // interval
    return reference_time + completed_transmissions * interval + interval


def update_jitter(num_servers: int) -> float:
    if num_servers < 100:
        jitter = 0.1
    elif num_servers < 300:
        jitter = 0.2
    elif num_servers < 700:
        jitter = 0.4
    else:
        jitter = 0.5
    return jitter


def send_sync_messages(interval: float, reference_time: float, num_servers: int):
    sync_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    while True:
        time.sleep(next_sync_time(interval, reference_time) - time.time())
        jitter = update_jitter(num_servers)

        payload = json.dumps({"reference_time": reference_time, "jitter": jitter}).encode('utf-8')
        for address in registration.get_registered_devices().values():
            print(f"Sending sync message to {address}")
            sync_socket.sendto(payload, address)
