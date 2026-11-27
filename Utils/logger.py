# 本地存储运行日志文件、日志 -> 操作弹窗

import logging
# 轮转日志处理器，用来做日志切割，因为“if not”的静态检查误报，可以加注释手动忽略
# noinspection PyUnusedImport
from logging.handlers import RotatingFileHandler
from Config import LOG_PATH

# 定义日志工具类
class GUILogger:
    """类中的构造函数，创建对象会自动运行：获取logger实例，设置日志级别，会忽略DEBUG日志"""
    def __init__(self):
        self.logger = logging.getLogger("EasyFile")
        self.logger.setLevel(logging.INFO)

        """防止重复添加handler，避免日志重复写入"""
        if not self.logger.handlers:
            """定义日志格式"""
            fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
            """实现日志切割，会最多保留5个5MB的旧日志备份"""
            fh = RotatingFileHandler(
                LOG_PATH,
                encoding="utf-8",
                maxBytes=5 * 1024 * 1024,
                backupCount=5
            )
            """给日志文件处理器绑定格式，并挂载在logger实例上；保存格式化器，统一获取时间"""
            fh.setFormatter(fmt)
            self.logger.addHandler(fh)
            self.formatter = fmt

    def info(self, msg: str):
        """构造INFO日志记录对象"""
        record = logging.LogRecord(
            name=self.logger.name,
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg=msg,
            args=(),
            exc_info=None
        )
        """
        # 使用logging的formatTime拿时间，和写入文件的时间来源完全一致
        time_str = self.formatter.formatTime(record, "%H:%M:%S")
        """
        """写入日志文件"""
        self.logger.info(msg)
        """
        # 返回GUI展示文本
        return f"[{time_str}] INFO: {msg}"
        """

    def warn(self, msg: str):
        record = logging.LogRecord(
            name=self.logger.name,
            level=logging.WARNING,
            pathname="",
            lineno=0,
            msg=msg,
            args=(),
            exc_info=None
        )
        """
        time_str = self.formatter.formatTime(record, "%H:%M:%S")
        """
        self.logger.warning(msg)
        """
        return f"[{time_str}] WARN: {msg}"
        """

    def error(self, msg: str):
        record = logging.LogRecord(
            name=self.logger.name,
            level=logging.ERROR,
            pathname="",
            lineno=0,
            msg=msg,
            args=(),
            exc_info=None
        )
        """
        time_str = self.formatter.formatTime(record, "%H:%M:%S")
        """
        self.logger.error(msg)
        """
        return f"[{time_str}] ERROR: {msg}"
        """

"""实例化全局日志对象"""
global_log = GUILogger()