_registered_devices = set()


def _register(device_id: int):
    global _registered_devices
    number_of_devices = len(_registered_devices)
    _registered_devices.add(device_id)
    if number_of_devices == len(_registered_devices):
        print(f"Devce with id={device_id} already registered, can not be registered!")
    else:
        print(f"Registered device {device_id}")


def _unregister(device_id: int):
    global _registered_devices
    number_of_devices = len(_registered_devices)
    _registered_devices.discard(device_id)
    if number_of_devices == len(_registered_devices):
        print(f"Device with id={device_id} not registered, can not be unregistered!")
    else:
        print(f"Unregistered device {device_id}")


def get_registered_devices() -> set[int]:
    global _registered_devices
    return _registered_devices


def handle_message(address: tuple[str, int], message: dict):
    print(f"handling registration message: {message}")

    if message['action'] == "register":
        _register(message['device_id'])
    elif message['action'] == "unregister":
        _unregister(message['device_id'])
