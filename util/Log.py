import logging
from colorlog import ColoredFormatter

class Log(object):
    def __init__(self, name=''):
        logger = logging.getLogger(name)
        # 定义输出格式
        consoleHandler = logging.StreamHandler()
        formatter = ColoredFormatter('%(log_color)s[%(asctime)s][%(name)s][%(levelname)s] %(message)s%(reset)s')
        consoleHandler.setFormatter(formatter)
        logger.addHandler(consoleHandler)

        logger.setLevel(level=logging.DEBUG)

        self.logger = logger
        pass
    
    def debug(self, text):
        self.logger.debug(text)

    def info(self, text):
        self.logger.info(text)

    def warn(self, text):
        self.logger.warning(text)

    def error(self, text):
        self.logger.error(text)

    def success(self, text):
        self.logger.critical(text)
