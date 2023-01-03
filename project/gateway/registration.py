__registered_devices = set()


def __register(device_id: int):
    global __registered_devices
    __registered_devices.add(device_id)
    print(f"Registered device {device_id}")


def __unregister(device_id: int):
    global __registered_devices
    __registered_devices.remove(device_id)
    print(f"Unregistered device {device_id}")


def get_registered_devices() -> set[int]:
    global __registered_devices
    return __registered_devices


def handle_message(message: dict):
    print(f"handling registration message: {message}")

    if message['action'] == "register":
        __register(message['device_id'])
    elif message['action'] == "unregister":
        __unregister(message['device_id'])
