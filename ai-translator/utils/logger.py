from loguru import logger
import os 
import sys

LOG_FILE = "app.log"
ROTATION_TIME= "02:00"

class Logger:
    def __init__(self, name="translation", log_dir="logs",debug=False):
        #日志目录不存在就需要创建
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        log_file_path = os.path.join(log_dir, LOG_FILE)

        #移除默认的logri handler
        logger.remove()

        # Add console handler with a specific log level
        level = "DEBUG" if debug else "INFO"
        logger.add(sys.stdout, level=level)
        # Add file handler with a specific log level and timed rotation
        logger.add(log_file_path, rotation=ROTATION_TIME, level="DEBUG")
        self.logger = logger

#这里设置日志的等级
LOG = Logger(debug=True).logger
