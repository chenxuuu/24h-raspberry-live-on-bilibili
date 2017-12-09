from util.Log import Log
import signal

from service.Media import MediaService
from service.Danmu import DanmuService
from service.Download import DownloadService

log = Log('Main')
mediaService = MediaService()
danmuService = DanmuService()
downloadService = DownloadService()

def exitHandler(signum, frame):
    log.success('请等待 Service 退出...')
    mediaService.stop()
    danmuService.stop()
    downloadService.stop()

if __name__ == '__main__':
    mediaService.start()
    danmuService.start()
    downloadService.start()

    signal.signal(signal.SIGINT, exitHandler)
    signal.signal(signal.SIGTERM, exitHandler)
