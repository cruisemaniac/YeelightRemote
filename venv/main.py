from Device import Device
from Helper import Helper
from Command import CommandHelper
from MainConfig import MainConfig
from tkinter import *
from tkinter.filedialog import askopenfilename
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


def load_config(show_dialog):
    global devices
    config = MainConfig()
    if os.path.isfile("yeelight.cfg"):
        devices = config.load()
    else:
        if show_dialog:
            config_file = askopenfilename(title="Config-Datei auswählen")
            if config_file:
                print(f"Config-Datei ausgewählt: {config_file}")
                devices = config.load(config_file)
    show_devices()


def show_devices():
    global devices, devices_framelabel

    if devices and len(devices) > 0:
        i = 0
        for device in devices:

            parent_framelabel = LabelFrame(devices_framelabel, text=device.display_name)
            parent_framelabel.grid(row=i)

            bulb_name = Label(parent_framelabel, text="device_name")
            bulb_name.grid(row=0, column=0, padx=5, pady=10)

            power_button = Button(parent_framelabel, text="An/Aus", command=lambda: send_toggle("test"))
            power_button.grid(row=0, column=1, padx=5, pady=10)

            rgb_button = Button(parent_framelabel, text="An/Aus", command=lambda: send_toggle("test"))
            rgb_button.grid(row=0, column=2, padx=5, pady=10)

            warmth_button = Button(parent_framelabel, text="An/Aus", command=lambda: send_toggle("test"))
            warmth_button.grid(row=0, column=3, padx=5, pady=10)

            brightness_slider = Scale(parent_framelabel, from_=0, to=100, orient=HORIZONTAL)
            brightness_slider.grid(row=0, column=4, rowspan=2, padx=5)

            delete_button = Button(parent_framelabel, text="An/Aus", command=lambda: send_toggle("test"))
            delete_button.grid(row=0, column=5, padx=5, pady=10)

            # Zur nächsten Reihe
            i = i+1
    else:
        print("Es können keine Geräte zum Anzeigen gefunden werden.")


def clear_devices():
    for child in devices_framelabel.winfo_children():
        child.destroy()


def send_toggle(test):
    print(test)
    ex_command = CommandHelper()

    if devices and len(devices) > 0:
        for device in devices:
            if device:
                device.set_command(ex_command.toggle_power())
                device.execute_command()


if __name__ == '__main__':
    main()
