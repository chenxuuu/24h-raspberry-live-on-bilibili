from downloader.NeteaseMusic import *

from service.Service import Service
from util.Danmu import Danmu
from util.Log import Log

from util.Queue import DownloadQueue
import time

class DanmuService(Service):
    
    def __init__(self):
        self.danmu = Danmu()
        self.log = Log('Danmu Service')
        self.commandMap = {
            '点歌': 'selectSongAction'
        }
        pass

    def run(self):
        self.parseDanmu()
        time.sleep(1.5)

    # 解析弹幕
    def parseDanmu(self):
        danmuList = self.danmu.get()
        if danmuList:
            for danmu in danmuList:
                self.log.debug('%s: %s' % (danmu['name'], danmu['text']))
                self.danmuStateMachine(danmu)

    # 将对应的指令映射到对应的Action上
    def danmuStateMachine(self, danmu):
        text = danmu['text']
        commandAction = ''
        for key in self.commandMap:
            # 遍历查询comand是否存在 若存在则反射到对应的Action
            if text.find(key) == 0 and hasattr(self, self.commandMap[key]):
                danmu['command'] = danmu['text'][len(key) : len(danmu['text'])]
                getattr(self, self.commandMap[key])(danmu)
                break
        pass

    def selectSongAction(self, danmu):
        self.log.info('%s 点歌 [%s]' % (danmu['name'], danmu['command']))
        DownloadQueue.put({ 'type': 'music', 'name': danmu['command'] })        
