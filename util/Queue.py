from queue import Queue

# 下载队列
class DownloadQueue:
    QueueInstance = Queue()

    @staticmethod
    def put(item, block=True, timeout=None):
        return DownloadQueue.QueueInstance.put(item, block=True, timeout=None)
    
    @staticmethod
    def get(block=True, timeout=None):
        return DownloadQueue.QueueInstance.get(block, timeout)

    @staticmethod
    def empty():
        return DownloadQueue.QueueInstance.empty()

# 播放队列
class PlayQueue:
    QueueInstance = Queue()

    @staticmethod
    def put(item, block=True, timeout=None):
        return PlayQueue.QueueInstance.put(item, block=True, timeout=None)
    
    @staticmethod
    def get(block=True, timeout=None):
        return PlayQueue.QueueInstance.get(block, timeout)

    @staticmethod
    def empty():
        return PlayQueue.QueueInstance.empty()

