---
title: 'Python 调用 Ansible API'
date: '2020-11-23T05:40:36+00:00'
status: private
permalink: /2020/11/23/python-%e8%b0%83%e7%94%a8-ansible-api
author: 毛巳煜
excerpt: ''
type: post
id: 6540
category:
    - Ansible
    - Python
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
###### 1\_init.yaml

```yaml
############################################################
# ansible-playbook -i inventory.ini 1_init.yaml -u root -k #
############################################################

- hosts: servers
  tasks:
    - name: 建立SSH互信
      authorized_key:
        user: "{{ username }}"
        key: "{{ lookup('file', lookup('env','HOME')+ '/.ssh/id_rsa.pub') }}"
        state: present

    - name: 设置hostame
      shell: hostnamectl set-hostname {{ inventory_hostname }}

    - name: RedHat 关闭防火墙
      service:
        name: firewalld
        state: stopped
        enabled: no
      when:
        - ansible_os_family == 'RedHat'

    - name: Debian 关闭防火墙
      service:
        name: ufw
        state: stopped
        enabled: no
      when:
        - ansible_os_family == 'Debian'


```

- - - - - -

###### inventory.ini

```ini
# 所有主机IP地址
[servers]
msy-master       ansible_ssh_user=root      ansible_ssh_host=192.168.22.26      ansible_ssh_port=40012    ansible_ssh_pass=123456
mqh-master      ansible_ssh_user=root      ansible_ssh_host=192.168.22.27      ansible_ssh_port=40006    ansible_ssh_pass=123456
wsx-master        ansible_ssh_user=root      ansible_ssh_host=192.168.22.28      ansible_ssh_port=40007    ansible_ssh_pass=123456
lzy-master          ansible_ssh_user=root      ansible_ssh_host=192.168.22.29      ansible_ssh_port=40008    ansible_ssh_pass=123456


[all:vars]
username = root


```

- - - - - -

- - - - - -

- - - - - -

###### 最简单的应用 playbook\_CLI.py

`./inventory.ini`、`./1_init.yaml` 测试访问放在与 playbook\_CLI.py同级目录

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 详细讲解： https://blog.csdn.net/u013613428/article/details/92837916

# ansible 源码API
from ansible.cli.playbook import PlaybookCLI


def main():
    cli = PlaybookCLI([" ", '-i', './inventory.ini', './1_init.yaml'])
    exit_code = cli.run()
    print(exit_code)


if __name__ == '__main__':
    main()


```

- - - - - -

- - - - - -

- - - - - -

###### 代码封装

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 详细讲解： https://blog.csdn.net/u013613428/article/details/92837916

from ansible import constants as C
from ansible.cli.playbook import PlaybookCLI
from ansible.plugins.callback import CallbackBase
import json
from ansible.cli import CLI
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible import context


class ResultCallback(CallbackBase):
    """
    一个示例回调插件，用于在返回结果时执行操作。
    如果要将所有结果在执行结束时收集到单个对象中，请考虑使用“json”回调插件，或者编写自己的自定义回调插件。
    """

    def __init__(self, *args, **kwargs):
        super(ResultCallback, self).__init__(*args, **kwargs)
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}

    # 运行成功
    def v2_runner_on_ok(self, result, *args, **kwargs):
        """
        打印结果的json表示。
        另外，将结果存储在实例属性中，以便以后检索
        """
        host = result._host
        self.host_ok[host.get_name()] = result
        # print('\033[32m %s \033[0m' % json.dumps({host.name: result._result}, indent=4))
        print('\033[32m %s %s \033[0m' % (result._task, '=' * 100))
        print('\033[32m %s \033[0m \n' % result._result)

    # 运行失败
    def v2_runner_on_failed(self, result, *args, **kwargs):
        host = result._host
        self.host_failed[host.get_name()] = result
        print('\033[31m %s %s \033[0m' % (result._task, '=' * 100))
        print('\033[31m ===运行失败==== \033[35m %s \033[31m ===result=%s \033[0m \n' % (host, result._result))

    # 无法访问
    def v2_runner_on_unreachable(self, result):
        host = result._host
        self.host_unreachable[host.get_name()] = result
        print('\033[31m %s %s \033[0m' % (result._task, '=' * 100))
        print('\033[31m ===无法访问====\033[35m %s \033[0m===result=%s \033[0m \n' % (host, result._result))

    # 跳过执行
    def v2_runner_on_skipped(self, result):
        if C.DISPLAY_SKIPPED_HOSTS:
            host = result._host.get_name()
            self.runner_on_skipped(host, self._get_item(getattr(result._result, 'results', {})))
            print('\033[35m %s %s \033[0m' % (result._task, '=' * 100))
            print('\033[35m ===跳过执行==== %s ===result=%s \033[0m \n' % (host, result._result))

    # 执行完成
    def v2_playbook_on_stats(self, stats):
        # print('\033[36m ===========executes completed======== \033[0m')
        print('\033[36m %s 执行完成 %s \033[0m \n' % ('=' * 50, '=' * 50))


# 定义入口函数
def main():
    # 远程节点机密码
    passwords = dict(vault_pass='pwd******')

    cli = PlaybookCLI([" ", '-i', './inventory.ini', './1_init.yaml'])

    super(PlaybookCLI, cli).run()
    # cli.run();

    loader, inventory, variable_manager = cli._play_prereqs()

    CLI.get_host_list(inventory, context.CLIARGS['subset'])

    pbex = PlaybookExecutor(
        playbooks=context.CLIARGS['args'], inventory=inventory
        , variable_manager=variable_manager, loader=loader, passwords=passwords)

    pbex._tqm._stdout_callback = ResultCallback()

    pbex.run()


if __name__ == '__main__':
    main()


```