import json


class Command:

    def __init__(self, method, parameters):
        self.cmd_id = uuid.uuid4().int
        self.method = method
        if parameters:
            self.parameters = parameters
        else:
            self.parameters = list() # Leere Liste erstellen falls keine Parameter geliefert werden.

    @cmd_id
    def cmd_id(self):
        return cmd_id

    def get_json(self):
        json_data = json.dumps({"id": self.cmd_id, "method": self.method, "params": self.parameters})
        print(json_data)
        return "json_data"
