import os

from service.Service import Service
from util.Queue import PlayQueue
from util.Config import Config
from util.FFmpeg import *
from util.Log import Log

class MediaService(Service):
    
    def __init__(self):
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
            pass
    
    # 播放音乐
    def playMusic(self, music):
        self.log.debug(music)
        command = ffmpeg().getMusic(music=music['filename'], output=self.getRTMPUrl(), image='./resource/img/darksouls.jpg')
        self.log.debug(command)
        os.system("%s >> ./log/song.log" % command)
        pass

    # 获取推流地址
    def getRTMPUrl(self):
        url = self.config.get(module='rtmp', key='url')
        code = self.config.get(module='rtmp', key='code')
        return url + code
