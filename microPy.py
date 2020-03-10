import machine
import math
import network
import os
import time
import utime
import gc
import ubinascii
import socket
from machine import RTC
from machine import SD
from L76GNSS import L76GNSS
from pytrack import Pytrack
from network import LoRa

lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)

app_eui = ubinascii.unhexlify("70B3D57ED001B609")

app_key = ubinascii.unhexlify("BD34EE4319780DB3E00BF55EC4EBB271")

lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)

s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

time.sleep(2)
gc.enable()

# setup rtc
rtc = machine.RTC()
rtc.ntp_sync("pool.ntp.org")
utime.sleep_ms(750)
print('\nRTC Set from NTP to UTC:', rtc.now())
utime.timezone(7200)
print('Adjusted from UTC to EST timezone', utime.localtime(), '\n')

py = Pytrack()
l76 = L76GNSS(py, timeout=30)

# sd = SD()
# os.mount(sd, '/sd')
# f = open('/sd/gps-record.txt', 'w')

while (True):
    coord = l76.coordinates()
    # f.write("{} - {}\n".format(coord, rtc.now()))
    print("{} - {} - {}".format(coord, rtc.now(), gc.mem_free()))
    coord = l76.coordinates()
    lat = str(coord[0])
    lng = str(coord[1])
    if lat is not "None":
        s.setblocking(True)
        msg = lat + "" + lng
        s.send(msg)
        s.setblocking(False)
    else:
        print("We did not get GPS lock yet.")
