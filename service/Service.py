import threading, time
import ctypes

class Service(object):
    def start(self):
        self.threadRun = True
        threading.Thread(target=self.__run).start()
    pass

    def stop(self):
        self.threadRun = False

    def __run(self):
        while self.threadRun:
            self.run()

    def run(self):
        self.stop()
        raise Exception('未实现 service 的 run 函数')

