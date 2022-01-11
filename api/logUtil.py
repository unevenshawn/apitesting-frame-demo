import datetime
import logging
import time

from api import yamlUtil, fileUtil


class LoggerUtil:
    logger = None

    def get_logger(self, logger_name: str = "log"):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)
        # 去除重复日志，如果不存在log handler才会需要创建，存在就调过
        if not self.logger.handlers:
            # 设置控制台日志控制器
            self.set_logger_hander()
            # 设置文件日志控制器
            self.set_logger_hander(isFileHandler=True)
        return self.logger

    def set_logger_hander(self, isFileHandler: bool = False):
        # 如果存在log_filepath,那么就是文件日志控制器
        logger_handler: logging.Handler = None
        if isFileHandler:
            log_filepath = fileUtil.join(yamlUtil.get_path(), "logs",
                                         str(yamlUtil.read_conf_yml("log", "log_name")) + str(
                                             (datetime.datetime.today().date())) + ".log")
            logger_handler = logging.FileHandler(filename=log_filepath, encoding="utf-8")
        else:
            # 创建对应的logger handler
            logger_handler = logging.StreamHandler()
        # 读取config.yml中的log level
        log_level = str(yamlUtil.read_conf_yml("log", "log_level")).lower()
        # 设置入handler中
        """
        CRITICAL = 50
        FATAL = CRITICAL
        ERROR = 40
        WARNING = 30
        WARN = WARNING
        INFO = 20
        DEBUG = 10
        NOTSET = 0
        """
        if log_level == "debug" or log_level == "10":
            logger_handler.setLevel(logging.DEBUG)
        elif log_level == "info" or log_level == "20":
            logger_handler.setLevel(logging.INFO)
        elif log_level == "warning" or log_level == "warn" or log_level == "30":
            logger_handler.setLevel(logging.WARN)
        elif log_level == "error" or log_level == "40":
            logger_handler.setLevel(logging.ERROR)
        elif log_level == "fatal" or log_level == "critical" or log_level == "50":
            logger_handler.setLevel(logging.CRITICAL)
        # 其余的情况，都按照debug级别设置
        else:
            logger_handler.setLevel(logging.DEBUG)
        # 创建日志格式,setFormatter，要传入Formatter的实例
        logger_handler.setFormatter(logging.Formatter(yamlUtil.read_conf_yml("log", "log_format")))
        # 将控制器加入到控制器对象中
        self.logger.addHandler(logger_handler)


# 错误日志输出
def error_log(message):
    LoggerUtil().get_logger().error(message)
    raise Exception(message)

# info日志输出
def info_log(message):
    LoggerUtil().get_logger().info(message)
