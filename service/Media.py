import os
import random
import subprocess

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
                # 获取随机文件，播放
                musicPath = './resource/music/'
                randomMusic = self.getRandomFile(musicPath)
                
                musicName = os.path.basename(randomMusic)
                musicName = musicName.replace(os.path.splitext(randomMusic)[1], '')

                self.playMusic({
                    'username': '系统',
                    'name': musicName,
                    'filename': musicPath + randomMusic
                }, True)
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
    def playMusic(self, music, autoPlay=False):
        imagePath = './resource/img/'
        randomImage = imagePath + self.getRandomFile(imagePath)
        self.log.info('[Music] 开始播放[%s]点播的[%s]' % (music['username'], music['name']))
        self.danmu.send('正在播放%s' % music['name'])
        
        # 获取歌词
        assPath = './resource/lrc/default.ass'
        if 'lrc' in music:
            assPath = music['lrc']

        # 开始播放
        command = ffmpeg().getMusic(music=music['filename'], output=self.getRTMPUrl(), image=randomImage, ass=assPath)
        command = "%s 2>> ./log/ffmpeg.log" % command
        self.log.debug(command)
        process = subprocess.Popen(args=command, cwd=os.getcwd(), shell=True)
        process.wait()
        
        # 播放完毕
        if not autoPlay:
            os.remove(path=music['filename'])
        self.log.info('[Music] [%s]播放结束' % music['name'])

    # 获取推流地址
    def getRTMPUrl(self):
        url = self.config.get(module='rtmp', key='url')
        code = self.config.get(module='rtmp', key='code')
        return url + code

    # 获取随机文件
    def getRandomFile(self, path):
        fileList = os.listdir(path)
        if len(fileList) == 0:
            raise Exception('无法获取随机文件，%s为空' % path)

        index = random.randint(0, len(fileList) - 1)
        return fileList[index]
