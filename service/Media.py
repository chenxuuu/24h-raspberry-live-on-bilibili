import os

from service.Service import Service
from util.Queue import PlayQueue
from util.Config import Config
from util.Danmu import Danmu
from util.FFmpeg import *
from util.Log import Log

class MediaService(Service):
    
    def __init__(self):
        self.danmu = Danmu()
        self.log = Log('Media Service')
        self.config = Config()

    def run(self):
        try:
            # 判断队列是否为空
            if PlayQueue.empty():
                return

            # 获取新的下载任务
            task = PlayQueue.get()
            if task and 'type' in task:
                if task['type'] == 'music':
                    self.playMusic(task)
                elif task['type'] == 'vedio':
                    pass

        except Exception as e:
            self.log.error(e)
    
    # 播放音乐
    def playMusic(self, music):

        self.log.info('[Music] 开始播放[%s]点播的[%s]' % (music['username'], music['name']))
        self.danmu.send('正在播放%s' % music['name'])
        # 开始播放
        command = ffmpeg().getMusic(music=music['filename'], output=self.getRTMPUrl(), image='./resource/img/darksouls.jpg')
        command = "%s 2>> ./log/ffmpeg.log" % command
        self.log.debug(command)
        os.system(command)
        # 播放完毕
        os.remove(path=music['filename'])
        self.log.info('[Music] [%s]播放结束' % music['name'])

    # 获取推流地址
    def getRTMPUrl(self):
        url = self.config.get(module='rtmp', key='url')
        code = self.config.get(module='rtmp', key='code')
        return url + code
