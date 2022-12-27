import json

class Register_message:
    def __init__(self, id, timestamp):
        self.action = "register"
        self.id = id
        self.timestamp = timestamp

    def to_json(self):
        return json.dumps(self.__dict__)
