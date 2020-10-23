import web_main_server
import web_auth_server


if IS_MAIN_SERVER:
  web_main_server.main(config, wifi, console, bme)

else:
  web_auth_server.main(config, wifi, console)
