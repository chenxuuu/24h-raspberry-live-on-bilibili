from util.Queue import DownloadQueue, PlayQueue

from downloader.NeteaseMusic import NeteaseMusic
from service.Service import Service
from util.Log import Log

class DownloadService(Service):
    
    def __init__(self):
        self.log = Log('Download Service')
        self.musicDownloader = NeteaseMusic()

    # 获取下载队列 分发至下载函数
    def run(self):
        try:
            # 判断队列是否为空
            if DownloadQueue.empty():
                return
            
            # 获取新的下载任务
            task = DownloadQueue.get()
            if task and 'type' in task:
                if task['type'] == 'music':
                    self.musicDownload(task)
                elif task['type'] == 'vedio':
                    pass
        except Exception as e:
            self.log.error(e)
            pass
    
    def musicDownload(self, item):

        # 搜索
        result = self.musicDownloader.search(item['name'])

        if result:
            # 搜索歌曲并下载
            song = result[0]
            songId = song['id']
            filename = self.musicDownloader.download(songId)

            if filename:
                singer = '未知歌手'
                if song['artists']:
                    singer = song['artists'][0]['name']
                self.log.info('歌曲下载完毕 %s - %s' % (song['name'], singer))

                # 加入播放队列
                PlayQueue.put({
                    'type': 'music',
                    'filename': filename,
                    'name': song['name'],
                    'singer': singer
                })
            else:
                pass

