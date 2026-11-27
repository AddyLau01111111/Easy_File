# Flet UI视图层（被动视图）：页面控件、布局、点击事件渲染，与业务逻辑（遍历文件夹、读取磁盘等）分离

import flet as ft
from typing import Callable, Optional
from .explorer_model import FileItem

# 定义UI视图类
class FileExplorerView:
    """接收回调函数（点击“上级”按钮，点击“显示隐藏文件”按钮，点击文件、文件夹卡片），存为实例，进行绑定"""
    def __init__(self, on_back, on_toggle_hidden, on_item_click):
        self.on_back = on_back
        self.on_toggle_hidden = on_toggle_hidden
        self.on_item_click = on_item_click

        """使用网格布局控件"""
        self.grid = ft.GridView(
            expand=True,
            runs_count=0,               # 窗口缩放自动适应列数
            max_extent=128,
            spacing=12,                 # 纵向间距
            run_spacing=12,             # 横向间距
            padding=16
        )

        self.current_path_text = ft.Text(
            "",
            size=12,                    # 地址栏文本大小
            color="#64748b",            # 文本颜色（前景色）
            no_wrap=True,               # 不换行，自动进行省略处理
            overflow=ft.TextOverflow.ELLIPSIS,
            tooltip=""                  # 悬浮显示完整路径
        )

        button_style = ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=6),      # 按钮统一样式（btn_back、btn_hidden）
            padding=ft.Padding(5.4, 0, 5.4, 9.6)            # 圆角、内边距
        )
        self.btn_back = ft.OutlinedButton(
            "👈",
            on_click=self.on_back,
            style=button_style
        )
        self.btn_hidden = ft.FilledButton(
            "显示隐藏文件",
            on_click=self.on_toggle_hidden,
            style=button_style
        )

        top_bar = ft.Container(
            ft.Row(
                [self.btn_back, self.btn_hidden, self.current_path_text],   # 顶部导航栏
                alignment=ft.MainAxisAlignment.START,                       # 元素左对齐
                spacing=10                                                  # 元素间距（横向）
            ),
            bgcolor="#ffffff",                                              # 背景色（背景分层）
            padding=ft.Padding(12, 8, 12, 8),                               # 内边距
            border=ft.Border(bottom=ft.BorderSide(1, "#e2e8f0"))            # 底部边框（底部分割线）
        )

        self.empty_state = ft.Container(
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.FOLDER_OPEN, size=64, color="#94a3b8"),
                    ft.Text("此文件夹为空", size=16, color="#64748b")
                ],                                                          # 空目录占位提示：图标+文本
                spacing=8,                                                  # 元素纵向间距
                alignment=ft.MainAxisAlignment.CENTER,                      # 元素垂直、水平居中
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            width=float("inf"),                                             # 宽度强制扩展撑满父容器
            alignment=ft.Alignment(0, 0)                                    # 内容水平居中对齐（左中右：-1、0、1；上中下：-1、0、1。垂直居中不生效）
        )

        self.content_area = ft.Column(
            [self.grid],
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            # horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0
        )                                                                   # 内容容器：占满self.view的剩余空间，子元素垂直居中（水平居中参数在本版本下兼容性不稳定）

        self.view = ft.Column(
            [
                top_bar,
                self.content_area
            ],                                                              # 组装页面结构：纵向排列
            expand=True,
            spacing=0
        )

    """悬浮事件处理"""
    def _on_card_hover(self, e):
        is_hover = e.data is True or str(e.data).lower() == "true"          # 避免小版本之间，e.data返回值类型不同的问题（布尔值、字符串）
        e.control.bgcolor = "#dbeafe" if is_hover else "#f8fafc"
        self.grid.update()                                                  # 刷新网格区域，触发完整重绘

    """接收FileItem列表，刷新网格"""
    def render_items(self, items: list[FileItem]):
        """清空网格中的旧卡片"""
        self.grid.controls.clear()

        if len(items) == 0:
            self.content_area.controls.clear()                              # 清空内容容器
            self.content_area.controls.append(self.empty_state)             # 空目录：内容为空状态（empty_state）
            return
        else:
            self.content_area.controls.clear()
            self.content_area.controls.append(self.grid)                    # 非空目录：内容为网格（grid）

        for item in items:
            icon = ft.Icon(
                ft.Icons.FOLDER_OPEN if item.is_dir else ft.Icons.INSERT_DRIVE_FILE,
                size=40,                                                    # 图标大小
                color="#2563eb" if item.is_dir else "#64748b"               # 图标颜色
            )

            """每个文件一个card：可点击（item挂载到控件的data属性上，将异步方法绑给on_click），包含图标和文件名（自动进行省略处理，文本居中对齐）"""
            card = ft.Container(
                content=ft.Column(
                    [
                        icon,
                        ft.Text(
                            item.name,
                            overflow=ft.TextOverflow.ELLIPSIS,
                            text_align=ft.TextAlign.CENTER,
                            size=12.5,              # 文本大小（文件、文件夹名称）
                            color="#1e293b"         # 文本颜色
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=4                       # 元素纵向间距
                ),
                data=item,
                on_click=self.on_item_click,
                padding=25,
                border_radius=8,                    # 圆角
                bgcolor="#f8fafc",                  # 背景颜色
                on_hover=self._on_card_hover
            )
            self.grid.controls.append(card)

    """更新地址栏地址"""
    def set_path_label(self, path: str):
        self.current_path_text.value = path
        self.current_path_text.tooltip = path       # 悬浮提示

    """将组装后的UI控件返回"""
    def build(self):
        return self.view