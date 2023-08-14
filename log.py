#encoding = utf-8

import logging


class Logger():
    def __init__(self, logname, loglevel=logging.DEBUG, loggername=None):
        '''
           指定保存日志的文件路径，日志级别，以及调用文件
           将日志存入到指定的文件中
        '''
        # 创建一个logger
        self.logger = logging.getLogger(loggername)
        self.logger.setLevel(loglevel)
        # 创建一个handler，用于写入日志文件
        fh = logging.FileHandler(logname)
        fh.setLevel(loglevel)
        if not self.logger.handlers:
            # 再创建一个handler，用于输出到控制台
            ch = logging.StreamHandler()
            ch.setLevel(loglevel)
            formatter = logging.Formatter(
                '[%(levelname)s]%(asctime)s %(filename)s:%(lineno)d: %(message)s')
            fh.setFormatter(formatter)
            ch.setFormatter(formatter)
            self.logger.addHandler(fh)
            self.logger.addHandler(ch)

    def getlog(self):
        return self.logger
