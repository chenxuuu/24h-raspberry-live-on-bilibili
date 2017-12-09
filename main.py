from util.Log import Log
from service.Danmu import DanmuService
from downloader.NeteaseMusic import *

import signal

music = NeteaseMusic()
songList = music.search('成都')
if songList:
    songId = songList[0]['id']
    print(music.getLyric(songId))

log = Log('Main')
danmuService = DanmuService()

def exitHandler(signum, frame):
    log.success('请等待 Service 退出...')
    danmuService.stop()

if __name__ == '__main__':
    # danmuService.start()

    signal.signal(signal.SIGINT, exitHandler)
    signal.signal(signal.SIGTERM, exitHandler)
