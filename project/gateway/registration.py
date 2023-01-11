_registered_devices = set()


def _register(device_id: int):
    global _registered_devices
    _registered_devices.add(device_id)
    print(f"Registered device {device_id}")


def _unregister(device_id: int):
    global _registered_devices
    _registered_devices.remove(device_id)
    print(f"Unregistered device {device_id}")


def get_registered_devices() -> set[int]:
    global _registered_devices
    return _registered_devices


def handle_message(message: dict):
    print(f"handling registration message: {message}")

    if message['action'] == "register":
        _register(message['device_id'])
    elif message['action'] == "unregister":
        _unregister(message['device_id'])
