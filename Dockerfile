FROM node:lts

WORKDIR /server-esp8266

COPY package.json /server-esp8266/package.json

RUN DEBIAN_FRONTEND=noninteractive apt-get update -q \
    && DEBIAN_FRONTEND=noninteractive apt-get install -qq -y \
      vim \
      nano \
      curl \
      screen \
      python3-pip \
    && pip3 install adafruit-ampy \
    && pip3 install rshell \
    && npm install --production \
    && npm install pm2 -g

COPY . /server-esp8266

CMD ["pm2-runtime", "ecosystem.config.js"]

EXPOSE 8000
