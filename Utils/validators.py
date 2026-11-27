#路径、权限校验

from pathlib import Path

# 判断路径是否存在且为文件
def is_file(path: Path) -> bool:
    try:
        return path.is_file()
    except OSError:
        return False

# 判断路径是否存在且为文件夹
def is_dir(path: Path) -> bool:
    try:
        return path.is_dir()
    except OSError:
        return False

# 简单判断目录是否可写
def is_writable() -> bool:
    try:
        """在当前目录下新建临时测试文件"""
        path = Path.cwd()
        test = path / ".write_test.tmp"
        test.touch(exist_ok=True)
        """删除测试文件"""
        test.unlink()
        return True
    except PermissionError:
        return False

# 判断目录是否可访问、可读
def is_readable(path: Path) -> bool:
    try:
        """只取出目标文件夹中的第一个文件，即可判断是否可以访问、读取（不完全严谨：next返回None无法证明目录可读）"""
        next(path.iterdir(), None)
        return True
    except PermissionError:
        return False