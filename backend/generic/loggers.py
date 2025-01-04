import datetime
import logging
import logging.handlers
import os


class DailyFileHandler(logging.handlers.RotatingFileHandler):
    def __init__(self, filename, *args, **kwargs):
        self._day = datetime.datetime.now().date()
        self._filename = filename
        self.try_mkdir_for_file(filename)
        filename = '%s.%s' % (self._filename, self._day)
        # 设置1G限制，最多保留5个
        super(DailyFileHandler, self).__init__(filename, maxBytes=1073741824, backupCount=5, *args, **kwargs)

    @staticmethod
    def try_mkdir_for_file(filename):
        folder = os.path.dirname(filename)
        if not os.path.exists(folder):
            os.makedirs(folder)

    def emit(self, record):
        day = datetime.datetime.now().date()
        if self._day != day:
            self._day = day
            self.close()
            self.baseFilename = '%s.%s' % (self._filename, self._day)
        super(DailyFileHandler, self).emit(record)
