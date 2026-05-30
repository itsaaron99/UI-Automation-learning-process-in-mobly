import time 
from data_models.wifi_protos import WifiConfig

class WifiController:
    
    def __init__(self, ad_device):
        """ Connects to a Wi-Fi network using the provided configuration. """
        self.ad = ad_device

    def connect(self, config: WifiConfig):
        ssid = str(config.ssid) if config.ssid else ""
        pwd = str(config.password) if config.password else None
        self.ad.log.info(f"WifiController: Connecting to SSID: '{ssid}' with PWD: '{pwd}'")

        if not ssid:
            self.ad.log.error("SSID is empty! Skipping connection.")
            return False

        if hasattr(self.ad, 'mbs'):
            try:
                if not self.ad.mbs.wifiIsEnabled():
                    self.ad.mbs.wifiEnable()
                    time.sleep(2)
                
                self.ad.mbs.wifiConnectSimple(ssid, pwd)
                return True
            except Exception as e:
                self.ad.log.error(f"Connection Fail: {e}")
                raise e