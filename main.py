# GUI界面地址栏输入str后，使用.strip()删除左右空格后，再转成Path实例（测试后添加）
# Easy File 的程序入口

import flet as ft
from GUI import ExplorerController

# Flet程序入口函数（将整个应用窗口根页面挂载在page上）
async def main(page: ft.Page):
    """页面基础配置"""
    page.title = "Easy File"
    page.padding = 0

    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(        # 全局主题：颜色方案
            primary="#2563eb",
            surface="#f8fafc",
            surface_container="#ffffff",
            on_surface="#1e293b",
            on_surface_variant="#64748b",
        ),
        scrollbar_theme=ft.ScrollbarTheme(  # 全局主题：滚动条主题
            thumb_color="#cbd5e1",
            track_color="#f1f5f9"
        ),
        font_family="Microsoft YaHei UI, Segoe UI, sans-serif"  # 全局主题：字体
    )
    page.bgcolor = page.theme.color_scheme.surface  # type: ignore

    """实例化控制器，创建好的视图渲染后，挂载到窗口页面上，并在“等待”后自动加载默认目录"""
    explorer = ExplorerController(page)
    page.add(explorer.view.build())
    await explorer.load_directory(explorer.current_path)

# 启动Flet应用
ft.run(main)