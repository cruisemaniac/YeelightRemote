import socket
import struct
import sys


def main():
    ssdp_adress = "239.255.255.250"
    ssdp_port = 1982

    ssdp_request = "M-SEARCH * HTTP/1.1\r\n" + \
                  "HOST: {adress}:{port}\r\n".format(adress=ssdp_adress, port=ssdp_port) + \
                  "MAN: \"ssdp:discover\"\r\n" + \
                  "ST: wifi_bulb\r\n"

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(ssdp_request.encode('utf-8'), (ssdp_adress, ssdp_port))
    while True:
        answer = sock.recv(1024)
        parse_answer(answer)
        if not answer:
            break
        answer = None
    sock.close()


def parse_answer(answer):
    answer = answer.decode("utf-8")
    readable_answer = answer.split("\\r\\n")

    # Ausgabe für Konsole // zum leichten debuggen
    for line in readable_answer:
        print(line)
    return readable_answer


if __name__ == '__main__':
    main()
