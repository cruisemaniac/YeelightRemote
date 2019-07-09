import pickle
import os.path

"""
Diese Klasse dient zum Speichern und Auslsen von der Yeelight Konfiguartionsdatei.
Die Konfiguartionsdatei wird als Binärdaten gespeichert und gelesen.
"""


class MainConfig:

    def __init__(self):
        self.devices = None

    def save(self):
        try:
            file = open("yeelight.cfg", "wb")
            pickle.dump(self.devices, file)
            print("Geräte wurden gespeichert!")
        except Exception as ex:
            # In dieser Methode soll diese Klasse als Datei gespeichert werden.
            print(f"Fehler beim Speichern der Geräte: Exception={ex}")
        finally:
            if file:
                file.close()

    def load(self):
        try:
            if os.path.isfile("yeelight.cfg"):
                file = open("yeelight.cfg", "rb")
                self.devices = pickle.load(file)
                print("Geräte wurden geladen!")
            else:
                print("Keine Config-Datei gefunden. Keine Geräte geladen.")
        except Exception as ex:
            print(f"Fehler beim Laden der Geräte: Exception={ex}")
        finally:
            if file:
                file.close()

