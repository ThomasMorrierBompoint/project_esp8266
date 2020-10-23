import network
import machine
import usocket
import ustruct
import utime
import uhashlib
import ubinascii
import bme280
import ssd1306
from env import config


class Wifi:
  def __init__(self):
    self.wlan = None

  # Connect to WiFi
  # This function could be improved has this it will never end until the connection is successful...
  def connect(self, ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(False)
    wlan.active(True)

    if not wlan.isconnected():
      wlan.connect(ssid, password)
      while not wlan.isconnected():
        pass

    self.wlan = wlan

  # Return the IP if wlan is connected
  @property
  def ip(self):
    if self.wlan and self.wlan.isconnected():
      return self.wlan.ifconfig()[0]
    else:
      return ''


class Console:
  def __init__(self, i2c, width=128, height=64):
    self.display = None
    self.width = width
    self.height = height
    self.y = 1
    # Initialize the SSD1306
    devices = i2c.scan()
    for device in devices:
      if device == 60:
        self.display = ssd1306.SSD1306_I2C(width, height, i2c, 0x3c)

  # Display messages using print and SSD1360 if possible
  # Use y_position if you need to append messages, in that case the SSD1306 screen wont be cleared
  def log(self, messages, y_position=1):
    # Ensure log will be easy to read
    print('\n_______________')

    # Ensure messages is an array not a string
    if isinstance(messages, str):
      messages = [messages]

    for message in messages:
      print(message)

    if self.display:
      self.y = y_position
      if self.y == 1:
        self.display.fill(0)
      for message in messages:
        if not isinstance(message, str):
          message = str(message)
        self.display.text(message, 1, self.y, 1)
        self.y += 10

    if self.display:
      self.display.show()

  # Display error messages
  def error(self, errors):
    # Ensure errors is an array not a string
    if isinstance(errors, str):
      errors = [errors]
    errors = ['Error:'] + errors
    self.log(errors)


class Clock:
  # Fetch time from pool.ntp.org by default
  @staticmethod
  def fetch_time(host='pool.ntp.org'):
    NTP_DELTA = 3155673600  # (date(2000, 1, 1) - date(1900, 1, 1)).days * 24*60*60
    NTP_QUERY = bytearray(48)
    NTP_QUERY[0] = 0x1B

    addr = usocket.getaddrinfo(host, 123)[0][-1]
    s = usocket.socket(usocket.AF_INET, usocket.SOCK_DGRAM)

    try:
      s.settimeout(1)
      res = s.sendto(NTP_QUERY, addr)
      msg = s.recv(48)
    except:
      s.close()
      return NTP_DELTA
    finally:
      s.close()

    val = ustruct.unpack("!I", msg[40:44])[0]
    return val - NTP_DELTA

  # Initialise the RTC (Independent clock that keeps track of the date and time)
  # RTC is set in UTC time so we need to add an offset for TZ (Time Zone -4h)
  @staticmethod
  def set_time():
    t = Clock.fetch_time()
    try:
      tm = utime.localtime(t - 14400)  # -4 * 60 * 60
      machine.RTC().datetime((tm[0], tm[1], tm[2], tm[6] + 1, tm[3], tm[4], tm[5], 0))
    except:
      pass

  # Get current time, use Util.set_time before using this function
  @staticmethod
  def get_time():
    try:
      now = utime.localtime()
      return (str(now[3]) + 'h' + str(now[4]) + 'm' + str(now[5]) + 's')
    except:
      return ''


class BME:
  def __init__(self, i2c):
    try:
      self.sensor = bme280.BME280(i2c=i2c)
    except:
      self.sensor = None

  @property
  def temperature(self):
    if self.sensor:
      return self.sensor.temperature
    else:
      return '0'

  @property
  def pressure(self):
    if self.sensor:
      return self.sensor.pressure
    else:
      return '0'

  @property
  def humidity(self):
    if self.sensor:
      return self.sensor.humidity
    else:
      return '0'


class Hash:
  @staticmethod
  def encrypt(string):
    string_hash = uhashlib.sha1(string)
    string_hash.update(config['SECRET_SALT'])
    string_hash = string_hash.digest()
    string_hash = ubinascii.hexlify(string_hash)
    return string_hash
