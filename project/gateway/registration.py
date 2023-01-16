from typing import Tuple, Dict

Address = Tuple[str, int]

_registered_devices: Dict[int, Address] = {}


def _register(address: Address, device_id: int):
    global _registered_devices

    if device_id in _registered_devices.keys():
        print(f"Device {device_id} already registered")
        return

    if address in _registered_devices.values():
        print(f"Device with address {address} already registered")
        return

    _registered_devices[device_id] = address
    print(f"Registered device {device_id} with address {address[0]}:{address[1]}")


def _unregister(device_id: int):
    global _registered_devices

    if device_id not in _registered_devices.keys():
        print(f"Can't unregister device {device_id} because it is not registered")
        return

    _registered_devices.pop(device_id)
    print(f"Unregistered device {device_id}")


def get_registered_devices() -> Dict[int, Address]:
    global _registered_devices
    return _registered_devices


def handle_message(address: Address, message: dict):
    if message['action'] == "register":
        _register(address, message['device_id'])
    elif message['action'] == "unregister":
        _unregister(message['device_id'])

__all__ = ["_register", "_unregister", "get_registered_devices", "handle_message"]


if __name__ == "__main__":
    pass


