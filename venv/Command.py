import json
import uuid
from random import randint


class CommandHelper:

    def __init__(self):
        self.cmd_id = uuid.uuid4().int % randint(13, 97)

    def set_power(self, turn_on):
        if turn_on:
            on_off = "on"
        else:
            on_off = "off"

        # effect = immer auf smooth, weil es so besser aussieht. 500 ist die Zeit in ms für den Übergang
        json_command = json.dumps({"id": self.cmd_id, "method": "set_power", "params": [on_off, "smooth", 500]})
        print(json_command)
        return json_command

    def toggle_power(self):
        print("NOCH NICHT IMPLEMENTIERT")

    def set_color(self):
        print("NOCH NICHT IMPLEMENTIERT")

    def set_warmth(self):
        print("NOCH NICHT IMPLEMENTIERT")

    def set_name(self):
        print("NOCH NICHT IMPLEMENTIERT")
