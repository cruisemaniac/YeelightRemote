import socket
import struct
import sys
import time
import uuid
from Device import Device
from Helper import Helper
from Command import CommandHelper
from MainConfig import MainConfig
from PyQt5.QtGui import *


def main():
    try:
        print("Suche gestartet.")
        helper = Helper()
        devices = helper.discover_devices(ssdp_adress="239.255.255.250", ssdp_port=1982)
        print("Suche abgeschlossen.")

        ex_command = CommandHelper()

        if devices and len(devices) > 0:
            for device in devices:
                if device:
                    device.set_command(ex_command.toggle_power())
                    device.execute_command()

    except Exception as ex:
        print(f"Fehler beim Ablauf des Programms. Exception={ex}")


if __name__ == '__main__':
    main()
