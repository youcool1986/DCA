import logging
from logging.handlers import TimedRotatingFileHandler
import os
from datetime import datetime

def log_set_up():
    # 定义日志级别关系映射
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }

    # 创建 logger 对象
    logger = logging.getLogger("Fa_range_trade")
    log_level = 'info'  # 假设从配置文件或其他地方获取日志级别
    logger.setLevel(level_relations.get(log_level, logging.INFO))  # 使用映射设置日志级别

    # 定义日志格式
    log_format = "%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s"

    # 创建一个用于写入日志文件的 handler
    log_filename = 'range_trade_log_file.txt'
    file_handler = TimedRotatingFileHandler(filename=log_filename, when='midnight', backupCount=30)
    file_handler.setFormatter(logging.Formatter(log_format))
    file_handler.setLevel(level_relations.get(log_level, logging.INFO))
    logger.addHandler(file_handler)

    # 创建一个用于输出到控制台的 handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(log_format))
    console_handler.setLevel(level_relations.get(log_level, logging.INFO))
    logger.addHandler(console_handler)

    return logger

# 使用日志系统
if __name__ == "__main__":

    logger = log_set_up()
    logger.info("start_running")
