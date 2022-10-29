import logging
import sys
import time
class LogOut(object):
    def __init__(self):
        self.logfile = (sys.argv[0]).replace(".py", "").replace("scripts","logs") + "-" + time.strftime("%Y%m%d") + ".log"
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter(
            "[ %(asctime)s ] - %(levelname)s - [ %(message)s ]",
            datefmt="%Y-%m-%d %H:%M:%S")
	
    def __outfile(self, level, msg):
        fh = logging.FileHandler(self.logfile, 'a', encoding='utf-8')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(self.formatter)
        self.logger.addHandler(fh)

       if level.upper() == "INFO":
            self.logger.info(msg)
       elif level.upper() == "ERROR":
            self.logger.error(msg)
       elif level.upper() == "WARNING":
            self.logger.warning(msg)
       elif level.upper() == "DEBUG":
            self.logger.debug(msg)
       else:
            self.logger.warning(msg)
            self.logger.removeHandler(fh)
	    fh.close()
	
    def debug(self, msg):
        self.__outfile('debug', msg)

    def info(self, msg):
        self.__outfile('info', msg)

    def warning(self, msg):
        self.__outfile('warning', msg)
	
    def error(self, msg):
        self.__outfile('error', msg) 
