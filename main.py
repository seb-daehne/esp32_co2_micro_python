import network
import urequests
import ujson 
import ubinascii 
from umqtt.simple import MQTTClient
from time import sleep_ms, ticks_ms, sleep
from machine import Pin, I2C
import time
import CCS811
import machine


def init():
    # ESP32 Pin assignment 
    pass

def publish(co2, tvoc):
    server = "192.168.1.248"
    
    client_id = ubinascii.hexlify(machine.unique_id())
    topic = "co2/sensor_1"

    value = {
        'co2': co2,
        'tvoc' : tvoc, 
        'id' : client_id
    }

    value_str = ujson.dumps(value)

    print("publishing to: " + topic)

    c = MQTTClient(client_id, server)

    c.connect()
    c.publish(topic, value_str)

    c.disconnect()


def connect_to_wifi():
    station = network.WLAN(network.STA_IF)
    station.active(True)

    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(False)

    station.connect("xxxx", "xxxx")
    print("connecting")

    while station.isconnected() != True:
        sleep(0.1)
    print("connected!")

    print(station.ifconfig())


print('init')
init()

print('connect to wifi')
connect_to_wifi()


print('sleep 10s')
i2c = I2C(scl=Pin(5), sda=Pin(4))
# Adafruit sensor breakout has i2c addr: 90; Sparkfun: 91
s = CCS811.CCS811(i2c=i2c, addr=90)
time.sleep(1)
while True:
    if s.data_ready():
        print('eCO2: %d ppm, TVOC: %d ppb' % (s.eCO2, s.tVOC))
        publish(s.eCO2, s.tVOC)
        time.sleep(1)

print('run app')


#machine.reset()