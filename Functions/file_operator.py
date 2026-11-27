# 文件操作，暂只支持同步扫描目录（不支持使用文件地址打开文件、不支持手动设置查不查看隐藏文件、文件夹大小显示问题）
import stat
from pathlib import Path
from Utils import global_log, is_file, is_dir

# 同步扫描目录
def scan_dir_sync(dir_path: Path, show_hidden: bool = False):
    items = []
    """确定输入的地址为目录"""
    if is_file(dir_path):
        raise NotADirectoryError(f"路径为文件: {dir_path}")
    if not is_dir(dir_path):
        raise FileNotFoundError(f"路径不存在: {dir_path}")
    """遍历目录下的文件、文件夹，拿到系统状态信息（跳过隐藏），将信息打包成字典，追加到items列表"""
    try:
        for entry in dir_path.iterdir():
            stat_info = entry.stat()
            """判断文件的隐藏属性"""
            is_hidden = bool(stat_info.st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN)
            if not show_hidden and is_hidden:
                continue
            items.append({
                "name": entry.name,
                "path": entry,
                "is_dir": entry.is_dir(),
                "size": stat_info.st_size,
                "mtime": stat_info.st_mtime
            })
        """按字母顺序排序，文件夹在前，普通文件在后（0->1，a->z）"""
        items.sort(key=lambda x: (not x["is_dir"], x["name"].lower()))
        return items
    except PermissionError:
        global_log.error(f"无权限访问：{dir_path}")
        raise PermissionError(f"权限不足，无法读取目录：{dir_path}")
    except Exception as e:
        global_log.error(f"扫描异常：{str(e)}")
        raise e