---
title: "Python使用子进程创建Web服务"
date: "2024-02-29"
categories: 
  - "python"
---

# 使用Python源生多进程模块，在子进程中创建Web服务

```python
from multiprocessing import Process

import uvicorn
from fastapi import FastAPI, Request
from starlette.responses import RedirectResponse


class ControlPlane:

    def __init__(self):
        # 使用Python的多进程模块创建子进程
        # 为多进程模块配置子进程服务
        self.child_process = Process(target=self.web_server)

    # 运行一个子进程启动Server
    @staticmethod
    def web_server():
        app = FastAPI()

        @app.get("/")
        async def root():
            # 访问根目录，默认跳转到SwaggerUI
            return RedirectResponse(url=f"http://127.0.0.1:8081/docs/")

        @app.get("/test_connection")
        async def get_status():
            return "success"

        uvicorn.run(app, host="127.0.0.1", port=8081)

    # 启动 FastChat Controller
    def start(self):
        # 启动子进程
        self.child_process.start()
        # 打印提示信息
        print("启动子进程")

    # 停止 FastChat Controller
    def stop(self):
        print("停止子进程")
        # 尝试温和地终止进程
        self.child_process.terminate()
        # 等待最多10秒
        self.child_process.join(10)

        # 如果进程仍然存活，强制终止进程
        if self.child_process.is_alive():
            print(f"{self.model_name} Terminate() 执行超时. 进程被强制杀死.")
            self.child_process.kill()
            self.child_process.join()  # 确保进程已经被结束

        # 关闭进程对象并释放资源
        self.child_process.close()
        print("关闭进程对象并释放资源")


if __name__ == "__main__":
    # 写一个存放服务的池
    server_pool = {}

    _app = FastAPI()


    @_app.get("/", summary="跳转到接口文档")
    async def root():
        # 访问根目录，默认跳转到SwaggerUI
        return RedirectResponse(url=f"http://127.0.0.1:8080/docs/")


    @_app.post("/start", summary="启动子进程服务")
    async def start(param="svc_0"):
        # 检查控制器池是否为空
        if not server_pool.get(param):
            server_pool[param] = ControlPlane()

            # 从控制器池中获取控制器
            server = server_pool[param]

            server.start()
            return "服务已启动"

        return "服务已存在"


    @_app.get("/stop", summary="停止子进程服务")
    async def stop(param="svc_0"):
        # 检查控制器池是否为空
        if server_pool.get(param):
            # 从控制器池中获取控制器
            service = server_pool[param]

            # 停止模型
            service.stop()

            # 从池中删除记录
            del server_pool[param]
            return "服务已关闭"

        return "服务不存在"


    uvicorn.run(_app, host="127.0.0.1", port=8080)

```
