import logging
import time
import os

"""
设置日至的级别和日志文件的格式
需要单例模式来节省内存
但logging模块自带单例模式
"""


def get_logger(logger_name):
    """
    :param logger_name:日志对象名称
    :return:返回logging对象
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    formatter_time = time.strftime('%Y%m%d%H', time.localtime(time.time()))
    formatter = logging.Formatter('%(asctime)s- %(name)s - '
                                  '%(filename)s:[line:%(lineno)s]- '
                                  '%(levelname)s - %(message)s')
    log_path = os.getcwd() + '/Logs/' + logger_name + '/'
    log_name = log_path + formatter_time + logger_name + '.log'
    fh = logging.FileHandler(log_name)
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger


# IP代理日志
proxy_logger = get_logger("proxy")
# 爬虫日志
spider_logger = get_logger("spider")
# 网路日志
net_logger = get_logger("net")
# 数据库日志
database_logger = get_logger("database")
