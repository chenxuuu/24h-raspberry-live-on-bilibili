from downloader.NeteaseMusic import *

from service.Service import Service
from util.Danmu import Danmu
from util.Log import Log

from util.Queue import DownloadQueue
import time

class DanmuService(Service):
    
    def __init__(self):
        self.danmu = Danmu()
        self.musicDownloader = NeteaseMusic()
        self.log = Log('Danmu Service')
        self.commandMap = {
            '点歌': 'selectSongAction',
            'id': 'selectSongByIdAction'
        }
        pass

    def run(self):
        try:
            self.parseDanmu()
            time.sleep(1.5)
        except Exception as e:
            self.log.error(e)

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

    # 歌曲名点歌
    def selectSongAction(self, danmu):
        self.log.info('%s 点歌 [%s]' % (danmu['name'], danmu['command']))

        command = danmu['command']
        song = []
        # 按歌曲名-歌手点歌
        if command.find('-') != -1:
            detail = command.split('-')
            if len(detail) == 2:
                song = self.musicDownloader.searchSingle(detail[0], detail[1])
            else:
                # 查询失败
                song = {}
                pass
        # 直接按歌曲名点歌
        else:
            song = self.musicDownloader.searchSingle(danmu['command'])

        if song:
            self.danmu.send('%s点歌成功' % song['name'])
            DownloadQueue.put({
                    'type': 'music',
                    'id': song['id'],
                    'name': song['name'],
                    'singer': song['singer'],
                    'username': danmu['name']
                })
        else:
            # 未找到歌曲
            self.danmu.send('找不到%s' % danmu['command'])
            self.log.info('找不到%s' % danmu['command'])
            pass

    # 通过Id点歌
    def selectSongByIdAction(self, danmu):
        command = danmu['command']
        try:
            song = self.musicDownloader.getInfo(command)
            if song:
                self.danmu.send('%s点歌成功' % song['name'])
                DownloadQueue.put({
                        'type': 'music',
                        'id': song['id'],
                        'name': song['name'],
                        'singer': song['singer'],
                        'username': danmu['name']
                    })
            else:
                # 未找到歌曲
                raise Exception('未找到歌曲')
        except Exception as e:
            self.danmu.send('找不到%s' % danmu['command'])
            self.log.info('找不到%s' % danmu['command'])