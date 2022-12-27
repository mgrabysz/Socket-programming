import json


class Register_message:
    def __init__(self, device_id, timestamp):
        self.action = "register"
        self.device_id = device_id
        self.timestamp = timestamp

    def to_json(self):
        return json.dumps(self.__dict__)


class Unregister_message:
    def __init__(self, device_id):
        self.action = "unregister"
        self.device_id = device_id

    def to_json(self):
        return json.dumps(self.__dict__)


class Transmission_message:
    def __init__(self, device_id, timestamp, payload):
        self.action = "transmit"
        self.device_id = device_id
        self.timestamp = timestamp
        self.payload = payload

    def to_json(self):
        return json.dumps(self.__dict__)
