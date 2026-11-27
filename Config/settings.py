# 全局配置、日志配置、弹窗配置

from pathlib import Path

# 全局配置
DEFAULT_ROOT_PATH = Path.home() / "Desktop"
SHOW_HIDDEN_FILE_DEFAULT = False
EXPLORER_PAGE_SIZE = 200

# 日志配置
LOG_PATH = Path("./app.log")

# 弹窗配置
DIALOG_TITLE_ERROR = "操作失败"
DIALOG_TITLE_WARN = "警告"