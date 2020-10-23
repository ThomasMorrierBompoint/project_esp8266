# This file is executed on every boot (including wake-boot from deepsleep)
from machine import I2C, Pin
from env import config
from util import Wifi, Console, Clock, BME
import gc

led = Pin(2, Pin.OUT)
led.off()

i2c = I2C(-1, Pin(5), Pin(4))
console = Console(i2c)

# Clear Serial Monitor
console.log(['', '', ''])
console.log('Hello from boot!')

console.log(' Init Wifi', console.y)
wifi = Wifi()
wifi.connect(config['SSID'], config['PASSWORD'])
console.log('IP: ' + wifi.ip, console.y)

IS_MAIN_SERVER = config['MAIN_SERVER_IP'] == wifi.ip
console.log('Is main: ' + str(IS_MAIN_SERVER), console.y)

console.log(' Init Clock', console.y)
Clock.fetch_time()
Clock.set_time()
current_time = Clock.get_time()
console.log(current_time, console.y)

bme = BME(i2c)

led.on()

gc.collect()
