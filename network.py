## Class for handling networking. 
import os
import gc
import ssl
import wifi
import socketpool
import adafruit_requests

class WifiNetwork:
    def __init__(self) -> None:
        self.RETRY_WIFI = 5 # Number of times to attempt to connect to wifi
        self.SSID = os.getenv('WIFI_SSID')
        self.PASS = os.getenv('WIFI_PASSWORD')

        if self.SSID is None or self.PASS is None or len(self.SSID) == 0 or len(self.PASS) == 0:
            raise Exception("WIFI_SSID & WIFI_PASSWORD are stored in settings.toml, please add them")

        self.connect()
   

    def connect(self) -> bool:
        """ If not connected connect to the network."""
        print("connecting to: {}".format(self.SSID))
        # TODO: async methods?
        attempt = 1
        while(attempt <= self.RETRY_WIFI):
            try:
                # TODO: async methods?
                wifi.radio.connect(self.SSID, self.PASS)                        
                return True
            except Exception as e:
                print(e)
            attempt += 1
        
        raise Exception('Unable to connect')
                  

    def getJson(self, url):
        try:
            pool = socketpool.SocketPool(wifi.radio)
            #context = ssl.create_default_context()
            #requests = adafruit_requests.Session(self._pool, self._context)
            requests = adafruit_requests.Session(pool, ssl.create_default_context())
            print('getting url:', url)
            gc.collect()
            print('free memory', gc.mem_free())

            
            try:
                #response = requests.get(url)
                response = requests.get(url, stream=True)
            except Exception as ex:
                print('Requests get()', ex)
                return {}
            print('free memory after', gc.mem_free())
            return response.json()
        except Exception as e:
            print('response.json Exception:', e)
            gc.collect()
        return {}        

    def get_interval(self):
        return int(self.INTERVAL)


    def get_pool(self):
        pass


