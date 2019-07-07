import socket
import struct
import sys
import time
from Device import Device


def main():
    print("Suche wird gestartet.")
    discoverd_devices = discover_devices(ssdp_adress="239.255.255.250", ssdp_port=1982)
    print("Suche abgeschlossen. Diese Geräte wurden entdeckt: ")

    if discoverd_devices is not None and len(discoverd_devices) > 0:
        for dev in discoverd_devices:
            print(dev)
            dev.connect()
            time.sleep(0.5)

    if discoverd_devices is not None and len(discoverd_devices) > 0:
        for dev in discoverd_devices:
            dev.disconnect()
            time.sleep(0.5)


def discover_devices(ssdp_adress, ssdp_port):
    """
    Diese Funktion sucht das Netzwerk nach Yeelight-Geräten ab. Für jedes gefundene Gerät wird ein
    Objekt erstellt. All diese Objekte werden in einer Liste zurückgegeben.
    :param ssdp_adress:
    :param ssdp_port:
    :return Liste von Yeelight-Geräten.
    """

    devices = list()

    try:
        ssdp_request = "M-SEARCH * HTTP/1.1\r\n" + \
                      f"HOST: {ssdp_adress}:{ssdp_port}\r\n" + \
                      "MAN: \"ssdp:discover\"\r\n" + \
                      "ST: wifi_bulb\r\n"
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(ssdp_request.encode('utf-8'), (ssdp_adress, ssdp_port))
        sock.settimeout(1)
        time.sleep(1)

        while True:
            try:
                answer = sock.recv(1024)  # 1024 Bytes lesen
            except socket.timeout:
                print(f"Timeout des Sockets nach {sock.gettimeout()}s. Es wird angenommen dass keine Daten mehr zu empfangen sind.")
                break;

            device_infolist = parse_ssdp_answer(answer, debug=False)
            device = create_device(device_infolist)

            if device and device_is_unique(device, devices):
                devices.append(device)

            #print(device)

            if not answer:
                break
            answer = None
            device = None

        return devices
    except Exception as ex:
        print(f"Fehler beim Senden oder Empfangen der SSDP Anfrage. Exception={ex}")
    finally:
        if sock:
            sock.close()


def parse_ssdp_answer(answer, debug):
    try:
        if answer:
            answer = answer.decode("utf-8")
            readable_answer = answer.splitlines()
        if debug:
            for line in readable_answer:  # Debug
                print(line)
        return readable_answer
    except Exception as ex:
        print(f"Fehler beim Verarbeiten der Antwort auf die SSDP Anfrage. Exception={ex}")
        return ""


def create_device(device_info):
    if device_info:
        try:
            location = device_info[4][10:]
            id = device_info[6][4:]
            model = device_info[7][7:]
            device = Device(device_id=id, location=location, model=model)
            return device
        except Exception as ex:
            print(f"Fehler bei Erstellung des Geräts(id={id} | location={location} | model={model}. Exception={ex}")
            return None

# Anhand der ID überprüfen ob es das Device schon gibt.
def device_is_unique(current_device, device_list):
    try:
        if len(device_list) > 0:
            for device in device_list:
                if device.device_id == current_device.device_id:
                    return False
        return True
    except Exception as ex:
        print(f"Fehler beim prüfen ob das Device schon gefunden wurde. Exception={ex}")

if __name__ == '__main__':
    main()
