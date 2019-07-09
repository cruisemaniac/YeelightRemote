import socket
from Command import CommandHelper

"""
Diese Klasse repräsentiert eine Yeelight Smartphone Lampe. In dieser Klasse speichern die jeweiligen Lampen
ihrem Namen, IP, Port, den Typen und viele weitere Sachen. Mit Hilfe von connect() und disconnect() kann
sich mit der Lampe verbunden werden um einen Befehl zu schicken.
"""


class Device:

    def __init__(self, device_id, ip, port, model):
        self.device_id = device_id  # Jede Lampe hat eine ID die als Hexadezimalzahl abgespeichert wird.
        self.ip = ip
        self.port = port
        self.model = model  # Model ist die Art der Lampe: Es gibt: color, desklamp
        self.display_name = "display_name"  # Anzeigename in der GUI-Anwendung
        self.command = None
        self.tcp_socket = None

    def __str__(self):
        if self.display_name:
            return f"Device (display_name={self.display_name}, " \
                f"model={self.model}, id={self.device_id}, location={self.ip}:{self.port})"
        else:
            return f"Device (model={self.model}, id={self.device_id}, location={self.ip}:{self.port})"

    def connect(self):
        try:
            print(f"Verbindungsaufsbau zu {self.ip}:{self.port}")

            sock = self.tcp_socket
            # Mit socket.SOCK_STREAM sagen wir dem Socket dass wir das TCP-Protokoll benutzen möchten.
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # sock.settimeout(1)
            sock.connect((self.ip, self.port))

            print("Verbindung erfolgreich aufgebaut!")
            return sock

        except Exception as ex:
            if sock:
                sock.close()
            print(f"Fehler beim Aufbau der TCP Verbindung. Exception={ex}")
            return None

    def disconnect(self, tcp_socket):
        try:
            if tcp_socket:
                tcp_socket.close()
                print("TCP-Verbindung erfolgreich geschlossen.")
        except Exception as ex:
            print(f"Fehler beim Schließen der TCP-Verbindung. Exception={ex}")

    # Mit Hilfe des CommandHelpers wird ein JSON erstellt, welches hier übergeben wird.
    def set_command(self, json_command):
        self.command = json_command

    def update(self):
        try:
            if self.tcp_socket:
                self.tcp_socket.listen()

        except Exception as ex:
            print(f"Fehler beim Aktualisieren des Status der Birne. Exception={ex}")

    # Beim Senden eines Commands wird geschaut ob es 1. einen Command gibt, und 2. das TCP-Socket eine Verbindung hat.
    # Nach jedem Command wird eine Verbindung hergestellt und auch wieder geschlossen.
    def execute_command(self):
        try:
            sock = self.tcp_socket
            if not self.command:
                print("Es gibt keinen Command der ausgeführt werden kann. "
                      "Es ist wohl etwas beim parsen des Befehls scheiefgelaufen")
                return

            # Nur ausführen falls es auch wirklich einen Command gibt. Falls es zum Beispiel ein Fehler beim
            # Erstellen des Commands gibt, wird nur ein leerer String zurückgegeben.
            if not sock:
                sock = self.connect()

            # Jeder Command muss mit einem Linebreak enden, sonst wird der Command nicht vom Gerät erkannt
            data = self.command + "\r\n"
            sock.send(bytes(data.encode("ascii")))
        except Exception as ex:
            print(f"Fehler beim Senden der Nachricht über TCP. Exception={ex}")
        finally:
            if sock:
                self.disconnect(sock)
