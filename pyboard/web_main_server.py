import time
import socket
import ujson
import urequests
from util import Clock, Hash


def main(config=None, wifi=None, console=None, bme=None):
  # Ensure messages from Boot.py are visible for at least 1 sec
  time.sleep(5)

  if config is None:
    config = ujson.loads('{"SECRET_SALT": "", "MAIN_SERVER_IP": ""}')

  ip = wifi.ip

  if not ip == config['MAIN_SERVER_IP']:
    console.error(['Invalid', 'Wifi or IP', ip, config['MAIN_SERVER_IP']])
    return

  # Socket listen to my current IP on port 80
  addr = socket.getaddrinfo(ip, 80)[0][-1]
  s = socket.socket()
  s.bind(addr)
  s.listen(1)
  console.log(['Init Main Server', addr])
  # Ensure messages is displayed for at least 2 sec
  time.sleep(2)

  while True:
    cl, addr = s.accept()

    data = cl.recv(4096)
    data = data.decode('utf-8')
    data = data.split('\n')
    data = data[0]
    password = data[0].split('/')

    # Validate password
    try:
      client_ip = addr[0]
      # client_ip_hash = Hash.encrypt(client_ip)
      # password_hash = Hash.encrypt(password)
      urequests.get('http://' + config['AUTH_SERVER_IP'] + '/' + client_ip)

      # if not response.text == 'True':
      #   cl.send('HTTP/1.0 401 OK\r\nContent-Type: text/plain\r\n\r\n')
      #   cl.send('401 Unauthorized')
      #   cl.close()
      #   continue

    except:
      cl.send('HTTP/1.0 401 OK\r\nContent-Type: text/plain\r\n\r\n')
      cl.send('401 Unauthorized')
      cl.close()
      continue

    current_time = Clock.get_time()
    temperature = bme.temperature
    pressure = bme.pressure
    humidity = bme.humidity
    console.log([current_time, 'Temperature', temperature, 'Pressure', pressure, 'Humidity: ' + humidity])

    response = ujson.dumps({
      'client_ip': client_ip,
      'password': password,
      'current_time': current_time,
      'temperature': temperature,
      'pressure': pressure,
      'humidity': humidity,
    })

    cl.send('HTTP/1.0 200 OK\r\nContent-Type: text/plain\r\n\r\n')
    cl.send(response)
    cl.close()


if __name__ == '__name__':
  main()
