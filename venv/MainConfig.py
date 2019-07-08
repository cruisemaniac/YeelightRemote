# Eine Klasse


class MainConfig:

    def __init__(self):
        self.device_list = None

    def save(self):
        try:
            print("MainConfig wird gespeichert!")

        except Exception as ex:
            # In dieser Methode soll diese Klasse als XML gespeichert werden.
            print(f"Fehler beim Speichern der MainConfig: Exception={ex}")

    def laod(self):
        try:
            # In dieser Methode soll diese Klasse von einem XML geladen werden.
            print("MainConfig wird geladen!")
        except Exception as ex:
            print(f"Fehler beim Speichern der MainConfig: Exception={ex}")

