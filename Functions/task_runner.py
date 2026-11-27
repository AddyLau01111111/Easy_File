# 封装异步库和线程池，确保Flet GUI不会主线程跑文件扫描卡界面（Flet是异步事件循环，文件扫描、操作等为同步阻塞函数）

import asyncio
from concurrent.futures import ThreadPoolExecutor
# 类型注解，Callable代表是一个函数，Any代表任意类型数据
from typing import Callable, Any

# 全局单例线程池，最多同时使用4个工作线程，处理所有耗时文件扫描、IO任务
_executor = ThreadPoolExecutor(max_workers=4)

# 异步函数定义（func -> 要执行的普通同步函数；callback -> 回调函数：成功传结果，失败传异常对象；*args -> 传给func的不定长参数）
async def run_background_task(func: Callable, callback: Callable[[Any], None], *args):
    """获取正在运行的asyncio事件循环（主线程中的Flet界面事件）"""
    loop = asyncio.get_running_loop()
    """在不影响主线程的情况下，子线程对同步阻塞函数进行处理，最后将处理结果传回主线程用于更新"""
    try:
        result = await loop.run_in_executor(_executor, func, *args)
    except Exception as e:
        callback(e)
        return
    callback(result)