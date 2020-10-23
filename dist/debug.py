from machine import Pin
import time

print('DEBUG')

led = Pin(2, Pin.OUT)
led.off()
time.sleep(2)
led.on()
