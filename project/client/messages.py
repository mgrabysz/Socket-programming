"""
Projekt PSI - System agregacji dokumentów
Autorzy: Marcin Grabysz
Data utworzenia: 27.12.2022
"""

import json
from typing import NamedTuple


class RegisterMessage:
    def __init__(self, device_id, timestamp):
        self.action = "register"
        self.device_id = device_id
        self.timestamp = timestamp

    def to_json(self):
        return json.dumps(self.__dict__)


class UnregisterMessage:
    def __init__(self, device_id):
        self.action = "unregister"
        self.device_id = device_id

    def to_json(self):
        return json.dumps(self.__dict__)


class TransmissionMessage:
    def __init__(self, device_id, timestamp, payload):
        self.action = "transmit"
        self.device_id = device_id
        self.timestamp = timestamp
        self.payload = payload

    def to_json(self):
        return json.dumps(self.__dict__)


class SyncMessage(NamedTuple):
    reference_time: float
    jitter: float

    @classmethod
    def from_json(cls, json_message):
        return cls(json_message['reference_time'], json_message['jitter'])


if __name__ == "__main__":
    pass
