import network
import asyncio
import json

class wifi_adapter:
    WIFI_DATA_FILE = "private_wifi.json"
    CONNECT_TRIES = 6

    def __init__(self):
        self.wlan = network.WLAN(network.STA_IF)

    async def connect(self, static_if_cfg = None, hostname = None):
        ssid, passwd = self.__get_wifi_cred(wifi_adapter.WIFI_DATA_FILE)

        if not all([ssid, passwd]):
            print("ssid/passwd not available can't connect.")
            return
        self.wlan.active(True)

        if hostname:
            network.hostname(hostname)
        if static_if_cfg:
            self.wlan.ifconfig(static_if_cfg)

        self.wlan.connect(ssid, passwd)
        print(f"Device hostname: {self.wlan.config("hostname")}")

        try_num = 0
        while (self.is_connected() == False and
               try_num < wifi_adapter.CONNECT_TRIES):
            try_num += 1
            print(f"WIFI Connecting... Try {try_num}/{wifi_adapter.CONNECT_TRIES}")
            await asyncio.sleep(2)

        if self.is_connected():
            print(f"WIFI Connection succeed. IP: {self.wlan.ifconfig()}")
        else:
            print(f"Couldn't connect to wifi named: {ssid}, check credential and make"
                  "sure device is in network range")

    def is_connected(self):
        return self.wlan.isconnected()

    def __get_wifi_cred(self, path):
        ssid = None
        passwd = None
        try:
            with open(path, "r") as file:
                j_file = json.load(file)
                ssid = j_file["ssid"]
                passwd = j_file["passwd"]
        except OSError:
            print(f"Could not open {path}")
        except KeyError as e:
            print(f"Key {e} missing in file")
        except json.JSONDecodeError:
            print("Could not decode json file. Might be corrupted.")

        return ssid, passwd
