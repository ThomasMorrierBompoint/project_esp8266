import time
import socket
import ujson
from util import Clock


def main(config=None, wifi=None, console=None):
  # Ensure messages from Boot.py are visible for at least 1 sec
  time.sleep(5)

  if config is None:
    config = ujson.loads('{"SECRET_SALT": "", "AUTH_SERVER_IP": ""}')

  ip = wifi.ip

  if not ip == config['AUTH_SERVER_IP']:
    console.error(['Invalid', 'Wifi or IP', ip, config['AUTH_SERVER_IP']])
    return

  # Socket listen to my current IP on port 80
  addr = socket.getaddrinfo(ip, 80)[0][-1]
  s = socket.socket()
  s.bind(addr)
  s.listen(1)
  console.log(['Init Auth Server', addr])
  # Ensure messages is displayed for at least 2 sec
  time.sleep(2)

  while True:
    cl, addr = s.accept()

    current_time = Clock.get_time()
    client_ip = addr[0]

    console.log([current_time, 'Request from', 'Client IP', client_ip])
    # TODO to be continued
    if client_ip == config['MAIN_SERVER_IP']:
      # Compare password to the list return True if authorize other wise return False
      cl.send('HTTP/1.0 200 OK\r\nContent-Type: text/plain\r\n\r\n')
      cl.send('True')
      cl.close()
    else:
      # Add password_hash to the list use the client_ip_hash to map
      cl.send('HTTP/1.0 200 OK\r\nContent-Type: text/plain\r\n\r\n')
      cl.send('Password added to the list')
      cl.close()


if __name__ == '__name__':
  main()
