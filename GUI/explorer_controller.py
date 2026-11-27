# 控制层（Flet UI的主线程）：连接UI（操作页面控件）、后台任务、数据，报错弹窗
# 大致逻辑：控制层被点击触发 -> Func后台处理 -> 数据传回控制层，在回调函数中使用数据 -> 视图层返回组装后的UI控件

import flet as ft
from pathlib import Path
from Config import DEFAULT_ROOT_PATH, SHOW_HIDDEN_FILE_DEFAULT, DIALOG_TITLE_ERROR
from Functions import run_background_task, scan_dir_sync
from Utils import global_log
from .explorer_model import FileItem
from .explorer_view import FileExplorerView

class ExplorerController:
    """控制器构造函数，包含：Flet的Page对象（这个应用界面，用来弹窗、刷新）、当前浏览的文件夹路径、标记是否展示隐藏文件"""
    def __init__(self, page: ft.Page):
        self.page = page
        self.current_path: Path = DEFAULT_ROOT_PATH
        self.show_hidden = SHOW_HIDDEN_FILE_DEFAULT

        """创建视图实例，将方法传给视图作为回调函数"""
        self.view = FileExplorerView(
            on_back=self.go_parent,
            on_toggle_hidden=self.toggle_hidden,
            on_item_click=self.on_item_click
        )

    """通用报错弹窗（需要先关闭弹窗再操作界面）"""
    def show_error_dialog(self, msg: str):
        dlg = ft.AlertDialog(
            title=ft.Text(DIALOG_TITLE_ERROR),
            content=ft.Text(msg),
            actions=[ft.TextButton("确定", on_click=lambda e: setattr(dlg, "open", False))],
            modal=True
        )
        dlg.open = True
        self.page.update()

    """加载目录（触发后台扫描目录）"""
    async def load_directory(self, target_path: Path):
        """回调：后台任务处理完成后回到主线程处理结果"""
        def handle_scan_result(res):
            if isinstance(res, Exception):
                global_log.error(str(res))
                self.show_error_dialog(str(res))
                self.page.update()
                return
            """检查扫描结果后，遍历生成数据模型对象列表，交给视图层进行视图更新"""
            file_items = [
                FileItem(
                    name=d["name"],
                    path=d["path"],
                    is_dir=d["is_dir"],
                    size=d["size"],
                    mtime=d["mtime"]
                ) for d in res
            ]
            self.view.render_items(file_items)
            self.view.set_path_label(str(target_path))
            self.current_path = target_path
            self.page.update()

        """（任务函数，完成后回调，任务函数参数1，任务函数参数2）"""
        await run_background_task(scan_dir_sync, handle_scan_result, target_path, self.show_hidden)

    """回调：返回上级目录（根目录点击无效）"""
    async def go_parent(self, e):
        parent = self.current_path.parent
        if parent != self.current_path:
            await self.load_directory(parent)

    """回调：切换显示隐藏文件开关"""
    async def toggle_hidden(self, e):
        self.show_hidden = not self.show_hidden
        await self.load_directory(self.current_path)

    """回调：点击打开（目前只支持文件夹 -> 后续在file_operator中处理打开文件）"""
    async def on_item_click(self, e):
        """从控件data中取出FileItem"""
        item = e.control.data
        if item.is_dir:
            await self.load_directory(item.path)
        else:
            print(f"选中文件：{item.path}")