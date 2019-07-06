import socket

class Device:

    def __init__(self, device_id, location, model):
        self.device_id = device_id  # Jede Lampe hat eine ID die als Hexadezimalzahl abgespeichert wird.
        self.location = location  # Location ist die Adresse der Lampe im Netzwerk
        self.model = model  # Model ist die Art der Lampe: Es gibt: color, desklamp
        self.display_name = ""  # Anzeigename in der GUI-Anwendung
        self.tcp_socket = None

    def __str__(self):
        if self.display_name:
            return f"Device (display_name={self.display_name}, model={self.model}, id={self.device_id}, location={self.location})"
        else:
            return f"Device (model={self.model}, id={self.device_id}, location={self.location})"

    def get_adress(self):
        try:
            return self.location
        except Exception as ex:
            print(f"Fehler beim Ermitteln der Adresse. Exception:{ex}")
            return "";

    def establish_tcp_connection(self, message):
        try:
            (ip, port) = self.get_adress()
            print(f"Verbindungsaufsbau zu {ip}:{port}")

            sock = self.tcp_socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            sock.connect((ip, port))

        except Exception as ex:
            print(f"Fehler beim Aufbau der TCP Verbindung. Exception={ex}")

    def send_command(self, command):
        try:
            sock = self.tcp_socket
            if sock:
                sock.send(message)

                try:
                    answer = s.recv(1024)
                    dec_answer = answer.decode("utf-8")
                except socket.timeout:
                    pass
            else:
                print("Es existiert keine Verbindung um eine Nachricht zu schicken.")

        except Exception as ex:
            print(f"Fehler beim Senden der Nachricht über TCP. Exception={ex}")