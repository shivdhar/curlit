import json


class Request:
    def __init__(self):
        self.body = None

    @property
    def json(self):
        return json.loads(self.body.decode('utf-8'))
