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

        get_new_uuid()
        # effect = immer auf smooth, weil es so besser aussieht. 500 ist die Zeit in ms für den Übergang
        json_command = json.dumps({"id": self.cmd_id, "method": "set_power", "params": [on_off, "smooth", 500]})
        print(json_command)
        return json_command

    def toggle_power(self):
        get_new_uuid()
        json_command = json.dumps({"id": self.cmd_id, "method": "toggle", "params": []})
        print(json_command)
        return json_command

    def set_color(self, rgb_color):
        if isinstance(rgb_color, int):
            if rgb_color > 16777215:
                rgb_color = 16777215
            if rgb_color < 0:
                rgb_color = 0

            get_new_uuid()
            json_command = json.dumps({"id": self.cmd_id, "method": "set_rgb", "params": [rgb_color, "smooth", 500]})
            print(json_command)
            return json_command
        else:
            print("Der Parameter \"rgb_color\" muss ein numerischer Wert "
                  "zwischen 0 (0x000000) und 16777215 (0xFFFFFF) sein.")
            return ""

    def set_brightness(self, brightness):
        if isinstance(brightness, int):
            if brightness > 100:
                brightness = 100
                print(f"Gegebener Wert war zu groß. Wert wurde auf {brightness} korrigiert")
            if brightness < 1:
                brightness = 1
                print(f"Gegebener Wert war zu groß. Wert wurde auf {brightness} korrigiert")

            get_new_uuid()
            json_command = json.dumps({"id": self.cmd_id, "method": "set_bright", "params": [brightness, "smooth", 500]})
            print(json_command)
            return json_command
        else:
            print("Der Parameter \"brightness\" muss ein numerischer Wert zwischen 1 und 100 sein.")
            return ""

    def set_color_temperature(self, temperature):
        if isinstance(temperature, int):
            if temperature > 6500:
                temperature = 6500
                print(f"Gegebener Wert war zu groß. Wert wurde auf {temperature} korrigiert")
            if temperature < 1700:
                temperature = 1700
                print(f"Gegebener Wert war zu groß. Wert wurde auf {temperature} korrigiert")

            get_new_uuid()
            json_command = json.dumps({"id": self.cmd_id, "method": "set_ct_abx", "params": [temperature, "smooth", 500]})
            print(json_command)
            return json_command
        else:
            print("Der Parameter \"brightness\" muss ein numerischer Wert zwischen 1 und 100 sein.")
            return ""

    def get_new_uuid(self):
        # Generiert eine neue Zufallszahl.
        self.cmd_id = uuid.uuid4().int % randint(13, 97)
