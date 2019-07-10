from Device import Device
from Helper import Helper
from CommandHelper import CommandHelper
from MainConfig import MainConfig
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.colorchooser import *
from tkinter.simpledialog import *
import os

# Initialisierung Variablen
devices = list()
helper = Helper()
devices_framelabel = None


def main():
    try:
        global devices_framelabel
        root = Tk()
        root.geometry("600x400")
        root.title("Yeelight Remote")
        load_button = Button(root, text="Config laden", command=lambda: load_config(show_dialog=True))
        load_button.pack(anchor="ne", padx=5, pady=5)

        save_button = Button(root, text="Config speichern", command=lambda: save_config())
        save_button.pack(anchor="ne", padx=5, pady=5)

        discover_button = Button(root, text="Geräte finden", command=discover)
        discover_button.pack(anchor="ne", padx=5, pady=5)
        devices_framelabel = LabelFrame(root, text="Geräte")
        devices_framelabel.pack(fill="both", expand="yes", pady=10, padx=10)

        # Config laden, aber automatisch kein Fenster öffnen
        load_config(show_dialog=False)

        root.mainloop()
    except Exception as ex:
        print(f"Fehler beim Ablauf des Programms. Exception={ex}")


def discover():
    global devices
    devices = helper.discover_devices(ssdp_adress="239.255.255.250", ssdp_port=1982)
    show_devices()


def load_config(show_dialog):
    global devices

    config = MainConfig()
    if os.path.isfile("yeelight.cfg"):
        devices = config.load(None)
    else:
        if show_dialog:
            config_file = askopenfilename(title="Konfigurationsdatei auswählen")
            if config_file:
                print(f"Konfigurationsdatei ausgewählt: {config_file}")
                devices = config.load(config_file)
    show_devices()


def save_config():
    if devices:
        config = MainConfig()
        config.save(devices)


def show_devices():
    global devices, devices_framelabel, button_dict

    if devices and len(devices) > 0:
        row_i = 0
        button_dict = dict()
        clear_devices()

        for device in devices:

            # Die Devices werden in der Reihenfolge in der sie hinzugefügt werden
            button_dict[row_i] = device

            # Falls das Gerät keinen Namen hat, soll das der Model-Name angezeigt werden.
            if device.display_name:
                framelabel_name = device.display_name
            else:
                framelabel_name = device.model

            parent_framelabel = LabelFrame(devices_framelabel, text=framelabel_name)
            parent_framelabel.grid(row=row_i, padx=10)

            bulb_name = Label(parent_framelabel, text=f"{row_i+1}.")
            bulb_name.grid(row=row_i, column=0, padx=5, pady=10)

            power_button = Button(parent_framelabel, text="An/Aus",
                                  command=lambda: send_toggle(parent_framelabel.grid_info()["row"]))
            power_button.grid(row=row_i, column=1, padx=5, pady=10)

            rgb_button = Button(parent_framelabel, text="RGB",
                                command=lambda: send_color(parent_framelabel.grid_info()["row"]))
            rgb_button.grid(row=row_i, column=2, padx=5, pady=10)

            warmth_button = Button(parent_framelabel, text="Temperatur",
                                   command=lambda: send_color_temperature(parent_framelabel.grid_info()["row"]))
            warmth_button.grid(row=row_i, column=3, padx=5, pady=10)

            brightness_slider = Scale(parent_framelabel, from_=0, to=100, orient=HORIZONTAL)
            brightness_slider.grid(row=row_i, column=4, rowspan=2, padx=5)
            brightness_slider.bind("<ButtonRelease-1>",
                                   lambda event, row=parent_framelabel.grid_info()["row"] : send_brightness(event, row))

            delete_button = Button(parent_framelabel, text="X", command=lambda: delete(parent_framelabel))
            delete_button.grid(row=row_i, column=5, padx=5, pady=10)

            # Zur nächsten Reihe
            row_i = row_i + 1
    else:
        print("Es können keine Geräte zum Anzeigen gefunden werden.")


def delete(parent_framelabel):
    parent_framelabel.destroy()


def clear_devices():
    for child in devices_framelabel.winfo_children():
        child.destroy()


def send_color_temperature(row):
    temperature_command = CommandHelper()

    dialog_result = askstring("Farbtemperatur", "Geben Sie einen Wert zwischen 1700 und 6500 ein.")

    if dialog_result and dialog_result.isdigit():
        temp = int(dialog_result)
    else:
        print("Bitte geben Sie nur numerische Werte ein")
        return

    if devices[row]:
        devices[row].execute_command(temperature_command.set_color_temperature(temp))


def send_brightness(event, row):
    brightness = event.widget.get()
    brightness_command = CommandHelper()

    if devices[row]:
        devices[row].execute_command(brightness_command.set_brightness(brightness))


def send_color(row):
    color_command = CommandHelper()
    _, hex_color = askcolor()  # Rückgabewert ist ein Tupel mit ((R,G,B), #Hex)
    if hex_color:
        hex_color = hex_color.replace("#", "")
        color_int = int(hex_color, 16)

        if devices[row]:
            devices[row].execute_command(color_command.set_color(color_int))


def send_toggle(row):
    toggle_command = CommandHelper()

    if devices[row]:
        devices[row].execute_command(toggle_command.toggle_power())


if __name__ == '__main__':
    main()
