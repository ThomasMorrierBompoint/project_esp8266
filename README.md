# ESP8266 (Only tested on Ubuntu)

- My port is `/dev/ttyUSB0` make sure you change the port on each command according to your setup.
- If you have a different port you need to change `ESP8266_PORT` in `./server.js` accordingly.
- In `./pyboard` create a file name `env.py`
    ```
    # Use this file to set your global/private config
    import ujson
    
    config = ujson.loads('{ "SSID": "", "PASSWORD": "", "SECRET_SALT": "SUPER_SECRET_KEY!", "AUTH_SERVER_IP": "", "MAIN_SERVER_IP": "" }')
    ```

### DOCKER

- Install/Start (then go to localhost:8000)
  ```
  docker-compose up
  ```
- Stop
  ```
  docker stop server-esp8266
  ```
- Delete
  ```
  docker rm server-esp8266
  ```
- Connect to the container with bash
  ```
  docker exec -it server-esp8266 bash
  ```

### Web interface

- RESET Button
  Remove all the files from your ESP8266 `/pyboard` and upload all the files from `./pyboard`
- DEBUG Button
  Run `./dist/debug.py` on your ESP8266
- SEND Button
  Upload the code from the WEB GUI to your ESP8266 `/pyboard/server-esp8266-script.py` and run it right away

### Screen

This part does not work inside the container not sure why but. I Guess it has to do with the command using the CTRL like (CTRL-a then c)

    ```
    screen /dev/ttyUSB0 115200
    ```

### Micropython

    ```
    # Create Firmware Backup
    python3 -m esptool --port /dev/ttyUSB0 read_flash 0x0 0x400000 ESP8266_org_4M.bin

    # Erase Firmware
    esptool.py --port /dev/ttyUSB0 erase_flash

    # Install Firmware Micropython
    esptool.py --port /dev/ttyUSB0 -b 115200 write_flash --flash_size=detect 0 esp8266-20200911-v1.13.bin

    # Deploy Firmware Backup
    python3 -m esptool --port /dev/ttyUSB0 read_flash 0x0 0x400000 ESP8266_org_4M.bin
    ```

# AMPY

Commands:

    ```
      get    Retrieve a file from the board.
      ls     List contents of a directory on the board.
      mkdir  Create a directory on the board.
      put    Put a file or folder and its contents on the board.
      reset  Perform soft reset/reboot of the board.
      rm     Remove a file from the board.
      rmdir  Forcefully remove a folder and all its children from the board.
      run    Run a script and print its output.
    ```

Test your ESP8266 connection

    ```
    ampy --port /dev/ttyUSB0 run dist/debug.py
    ```

# Reshell

    ```
    rshell
    connect serial /dev/ttyUSB0
    ```
