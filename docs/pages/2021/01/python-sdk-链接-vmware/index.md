---
title: "Python SDK 链接 VMware"
date: "2021-01-04"
categories: 
  - "python"
  - "vmware"
---

```python
import ssl
# https://zhuanlan.zhihu.com/p/58120047
# 用于注册程序退出时的回调函数
import atexit

from pyVmomi import vim
from pyVim import connect


class VMConnect(object):

    def __init__(self):
        # 配置ssl
        sslcontext = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        sslcontext.verify_mode = ssl.CERT_NONE
        # 连接到vcenter
        service_instance = connect.SmartConnect(
            host="192.168.14.154",
            port=443,
            user="root",
            pwd="123456",
            sslContext=sslcontext)
        # 注册程序退出时的回调
        atexit.register(connect.Disconnect, service_instance)
        # 链接vCenter
        self.content = service_instance.RetrieveContent()

    def get_info(self):

        # 获取执行信息
        container = self.content.rootFolder
        view_type = [vim.VirtualMachine]
        recursive = True
        container_view = self.content.viewManager.CreateContainerView(container, view_type, recursive)
        children = container_view.view

        # 统计机器数量
        on_num: int = 0
        off_num = 0

        # 输出信息
        if not children:
            print("no virtual_machine")
        for child in children:
            summary = child.summary

            # 判断是否为模板
            if summary.config.template:
                print("Name     : ", summary.config.name)
                print("PowerState     : ", summary.runtime.powerState)
                print("\n")
                continue

            # 在线
            if 'poweredOn' == summary.runtime.powerState:
                on_num = on_num + 1
            # 离线
            elif 'poweredOff' == summary.runtime.powerState:
                off_num = off_num + 1

        print(f'共有{len(children)}台虚拟机')
        print(f'在线{on_num}台虚拟机')
        print(f'离线{off_num}台虚拟机')


if __name__ == '__main__':
    # VMConnect()
    VMConnect().get_info()

```
