import json


class Command:

    def __init__(self, cmd_id, method, parameters):
        self.cmd_id = cmd_id
        self.method = method
        if parameters:
            self.parameters = parameters
        else:
            self.parameters = list()


    def create_json(self):
        json_data = json.dumps({"id": self.cmd_id, "method": self.method, "params": self.parameters})
        print(json_data)
        return "json_data"
