import pickle
import os.path

"""
Diese Klasse dient zum Speichern und Auslsen von der Yeelight Konfiguartionsdatei.
Die Konfiguartionsdatei wird als Binärdaten gespeichert und gelesen.
"""


class MainConfig:

    def save(self, devices):
        try:
            file = open("yeelight.cfg", "wb")
            if file:
                pickle.dump(devices, file)
                print("Geräte wurden gespeichert!")
        except Exception as ex:
            # In dieser Methode soll diese Klasse als Datei gespeichert werden.
            print(f"Fehler beim Speichern der Geräte: Exception={ex}")
        finally:
            if file:
                file.close()

    def load(self, alternative_file):
        file = None
        try:
            if os.path.isfile("yeelight.cfg"):
                file = open("yeelight.cfg", "rb")
                print("Geräte wurden geladen!")
                return pickle.load(file)
            else:
                print("Keine Config-Datei gefunden. Keine Geräte geladen.")
        except Exception as ex:
            print(f"Fehler beim Laden der Geräte: Exception={ex}")
        finally:
            if file:
                file.close()

