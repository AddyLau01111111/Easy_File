# 封装文件信息数据模型

# 用于快速创建数据类（自动生成__init__等方法）
from dataclasses import dataclass
from pathlib import Path
# 控制变量类型可选（int | None等）
from typing import Optional

# 将文件、文件夹的信息打包成一个对象，方便传递；“@property”将获取文件后缀方法转变成属性，调用时无需“()”
@dataclass
class FileItem:
    name: str
    path: Path
    is_dir: bool
    size: Optional[int]
    mtime: Optional[float]

    @property
    def suffix(self):
        return self.path.suffix.lower()