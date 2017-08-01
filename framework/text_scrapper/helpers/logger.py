import datetime
import logging
import os
import time
from urlparse import urlparse

class AppLogger:
    def __init__(self, channel):
        path_url = urlparse(channel)

        log_filename = str(path_url.netloc).replace(".", "_")  # normalize the domainname

        self.log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        # self.log_format = '%(levelname)s:%(asctime)s %(message)s'  # Log format
        working_dir = os.path.dirname(__file__)+"/../../log/"+log_filename
	    #working_dir = "/home/samshrestha/framework_PLD/log/"+log_filename
        self.output_filename = "{}-{}.log".format(working_dir, datetime.date.today())

        self.logger = None
        self.channel = channel
	#print('init complete')

    def get_logger(self, level):
        logger = logging.getLogger(self.channel)
        logger.setLevel(level)
        # create a file handler
	print(self.output_filename)
        handler = logging.FileHandler(self.output_filename)
	print('filehandler fails')

        handler.setLevel(level)

        # create a logging format

        formatter = logging.Formatter(self.log_format)
        handler.setFormatter(formatter)
	print('log format created')
        # add the handlers to the logger
        logger.addHandler(handler)

        self.logger = logger
        return logger

    @staticmethod
    def log(message):
        app_logger = AppLogger("application")
        app_logger.get_logger(logging.DEBUG).debug(message)

if __name__=="__main__":
    pass