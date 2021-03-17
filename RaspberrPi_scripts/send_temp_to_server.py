import socket
import struct
import time
from threading import Thread

from mlx90614 import MLX90614
from smbus2 import SMBus

global temp
import relay_control


def read_temp():
    while True:
        bus = SMBus(1)
        sensor = MLX90614(bus, address=0x5A)
        global temp
        # print (sensor.get_ambient())
        temp = sensor.get_object_1()
        # print (temp)
        byte_value = bytearray(struct.pack("f", temp))
        send_mesaj(byte_value)
        time.sleep(0.1)

        bus.close()
    return temp


def send_mesaj(msg):
    # Socket oluşturulması
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        host = "192.168.0.100"
        port = 8001

        try:
            s.connect((host, port))
            s.sendall(msg)
            # print(str(s.recv(1024), 'utf-8'))
            rec_msg = str(s.recv(1024), 'utf-8')
            relay_call(rec_msg)
        except socket.error as msg:
            print("[Server aktif değil.] Mesaj:", msg)
            relay_call("off-off")
        finally:
            s.close()


def relay_call(msg):
    start_th = Thread(target=relay_control.led_control, args=(msg,))
    start_th.deamon = True
    start_th.start()


if __name__ == "__main__":
    read_temp()
