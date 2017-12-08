from service.Service import Service
from util.Danmu import Danmu
from util.Log import Log
import time

class DanmuService(Service):
    
    def __init__(self):
        self.danmu = Danmu()
        self.log = Log('Danmu Service')
        pass

    def run(self):
        self.parseDanmu()
        time.sleep(1.5)

    # 解析弹幕
    def parseDanmu(self):
        danmuList = self.danmu.get()
        self.log.info(danmuList)
        pass
