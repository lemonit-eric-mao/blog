---
title: "Ansible-playbook 高级用法"
date: "2019-09-11"
categories: 
  - "ansible"
---

###### 通用 `hosts.ini`

```ruby
[servers]
# 别名 ansible_ssh_user=远程用户 ansible_ssh_host=远程IP ansible_ssh_port=22 ansible_ssh_pass=指定密码
master1-etcd1         ansible_ssh_host=192.168.20.91
master2-etcd2         ansible_ssh_host=192.168.20.92
master3-etcd3         ansible_ssh_host=192.168.20.93
worker                ansible_ssh_host=192.168.20.94
HAProxy1              ansible_ssh_host=192.168.20.95
HAProxy2              ansible_ssh_host=192.168.20.96

[all:vars]
username = root
deploy_dir = /home/deploy/offline_setup
ntp_server = pool.ntp.org

```

* * *

###### 通用 `inventory.ini`

```ini
[HAProxy]
HAProxy1 ansible_ssh_host=192.168.20.95
HAProxy2 ansible_ssh_host=192.168.20.96

[KeepAlived]
KeepAlived1 ansible_ssh_host=192.168.20.95
KeepAlived2 ansible_ssh_host=192.168.20.96

[etcd]
etcd1 ansible_ssh_host=192.168.20.91
etcd2 ansible_ssh_host=192.168.20.92
etcd3 ansible_ssh_host=192.168.20.93

[master]
master1 ansible_ssh_host=192.168.20.91
master2 ansible_ssh_host=192.168.20.92
master3 ansible_ssh_host=192.168.20.93

[worker]
worker1 ansible_ssh_host=192.168.20.94


[all:vars]
username = root
cluster_name = eric-es-cluster
deploy_dir = /home/elasticsearch/deploy
VirtualIP = 192.168.20.97
K8sVersion = 1.16.6
etcd_version = 3.3.8

```

* * *

* * *

* * *

###### 常用模块

```yaml
- hosts: servers
  tasks:


    # 在目标主机创建文件或目录，并赋予其系统权限
    - name: create a file
      file:
        path: '/root/foo.txt'
        # state:
        #        directory   表示创建目录
        #        link        表示创建软连接，link还需要源路径和目标路径配合使用
        #        touch       表示创建文件
        #        absent      表示删除文件
        state: touch
        mode: 0755
        owner: root
        group:  root


    - name: '将本地拷贝文件至各主机'
      copy:
        src: '源文件地址'
        dest: '远程主机地址'


    - name: '从各主机拷贝文件到本地'
      fetch:
        # 远程主机的文件，必须是文件，不能是目录
        src: "/home/demo.sh"
        # 文件要保存到的目录
        dest: "/home/deploy"
        flat: "yes"


    - name: 'wget url 下载'
      get_url:
        url: 'http://qiniu.dev-share.top/foo.zip'
        # 下载文件到指定目录
        dest: '/tmp/qiniu/'


    - name: '比get_url功能更强大的http请求模块，可以发起get、post、put等各种请求方式，也可以处理返回值及内容'
      uri:
        url: "http://qiniu.dev-share.top/foo.zip"
        method: GET
        # 下载文件到指定目录
        dest: '/tmp/qiniu/'


    - name: 'unzip 解压'
      unarchive:
        src: '/tmp/qiniu/foo.zip'
        dest: '/home/deploy/'
        # 在解压文件之前，是否先将文件复制到远程主机，默认为yes。
        # 若为no，则要求目标主机上压缩包必须存在。
        copy: no
        # 解压后文件的权限
        mode: 777
        # 解压后的目录或文件的属组
        grop: 'docker'


    - name: '执行脚本'
      shell: 'mkdir -p {{ deploy_dir }}/data/'


    - name: '启动 nginx'
      service:
        # name：     必选项，服务名称
        # state：    对当前服务执行启动，停止、重启、重新加载等操作（started,stopped,restarted,reloaded）
        # pattern：  定义一个模式，如果通过status指令来查看服务的状态时，没有响应，就会通过ps指令在进程中根据该模式进行查找，如果匹配到，则认为该服务依然在运行
        # runlevel： 运行级别
        # sleep：    如果执行了restarted，在则stop和start之间沉睡几秒钟
        # enabled：  是否开机自启动  yes|no
        name: nginx
        state: started
        enabled: yes


    - name: '安装多个工具'
      yum:
        name: {{ item }}
        ignore_errors: yes
        state: absent
      # 迭代下面的item，循环执行 yum
      loop:
        - epel-release
        - htop
        - vim
        - wget
        - net-tools


    - name: '等待事情发生，例如等待数据库启动、web容器启动等'
      wait_for:
        # connect_timeout：   在下一个任务执行之前等待连接的超时时间
        # delay：             等待一个端口或者文件或者连接到指定的状态时，默认超时时间为300秒，在这等待的300s的时间里，wait_for模块会一直轮询指定的对象是否到达指定的状态，delay即为多长时间轮询一次状态。
        # timeout：           wait_for的等待的超时时间,默认为300秒
        # host：              wait_for模块等待的主机的地址，默认为127.0.0.1
        # port：              wait_for模块待待的主机的端口
        # path：              文件路径，只有当这个文件存在时，下一任务才开始执行，即等待该文件创建完成
        # state：             等待的状态，即等待的文件或端口或者连接状态达到指定的状态时，下一个任务开始执行。
        #                         当等的对象为端口时，状态有started，stoped，即端口已经监听或者端口已经关闭；
        #                         当等待的对象为文件时，状态有present或者started，absent，即文件已创建或者删除；
        #                         当等待的对象为一个连接时，状态有drained，即连接已建立。默认为started
        port: 53
        timeout: 10


    - name: 修改文件内容
      lineinfile:
        # 必须参数，指定要操作的文件。
        dest: /etc/sudoers
        # 使用此参数指定文本内容。
        line: '{{ username }} ALL=(ALL) NOPASSWD: ALL'
        # 借助insertafter参数可以将文本插入到“指定的行”之后，
        # insertafter参数的值可以设置为EOF或者正则表达式，EOF为End Of File之意，
        # 表示插入到文档的末尾，默认情况下insertafter的值为EOF，
        # 如果将insertafter的值设置为正则表达式，表示将文本插入到匹配到正则的行之后，
        # 如果正则没有匹配到任何行，则插入到文件末尾，当使用backrefs参数时，此参数会被忽略。
        insertafter: EOF
        # 使用正则表达式匹配对应的行，当替换文本时，如果有多行文本都能被匹配，则只有最后面被匹配到的那行文本才会被替换，
        # 当删除文本时，如果有多行文本都能被匹配，这么这些行都会被删除。
        regexp: '^{{ username }} .*'
        # 当想要删除对应的文本时，需要将state参数的值设置为absent，absent为缺席之意，表示删除，state的默认值为present。
        state: present


    - name: '新增/替换 多条文件内容'
      lineinfile:
        dest: '/etc/sysctl.d/k8s.conf'
        line: '{{ item.key }} = {{ item.value }}'
        regexp: '^{{ item.key }}.*'
        state: present
      # 定义集合，并循环执行所在的模块
      with_items:
        - { key: "net.bridge.bridge-nf-call-ip6tables", value: "1" }
        - { key: "net.bridge.bridge-nf-call-iptables", value: "1" }


    - name: '只执行一次'
      # 只执行一次
      # 场景： 因为安装 etcd高可用时， 是要先初始化集群中第一个节点，然后在将其它的节点加入到集群中，而不是同时初始化为单独的服务
      run_once: true
      service:
        name: etcd
        state: started
        enabled: yes


    - name: '只在本地执行'
      gather_facts: false
      # 指定远程连接主机的方式，默认是ssh
      # 设置为local时，则只在本地执行
      connection: local
      run_once: true
      file:
        path: '/home/deploy/eric.txt'
        state: touch
        mode: 0755

```

* * *

* * *

* * *

###### 获取 inventory\_hostname 与 IP

`inventory_hostname`与`hostvars` 是ansible-playbook的内置变量

```yaml
#######################################################
# ansible-playbook -i hosts.ini show-hostname-ip.yaml #
#######################################################

- hosts: servers
  tasks:
    - name: 显示获取的 inventory_hostname 与 IP
      debug:
        msg: "{{ inventory_hostname }} === {{ hostvars[inventory_hostname].ansible_ssh_host }}"

```

* * *

* * *

* * *

###### 指定某个主机

```yaml
###########################################################
# ansible-playbook -i inventory.ini show-hostname-ip.yaml #
###########################################################

- hosts: master[0]
  tasks:
    - name: 显示获取的 inventory_hostname 与 IP
      debug:
        msg: "{{ inventory_hostname }} === {{ hostvars[inventory_hostname].ansible_ssh_host }}"

```

* * *

###### 逻辑判断

```yaml
###########################################################
# ansible-playbook -i inventory.ini show-hostname-ip.yaml #
###########################################################

- hosts: master
  tasks:
    - name: 逻辑判断
      debug:
        msg: "{{ inventory_hostname }} === {{ hostvars[inventory_hostname].ansible_ssh_host }}"
      # 当IP地址是master1的时候才执行
      when:
        - hostvars[groups.master[0]].ansible_ssh_host == hostvars[inventory_hostname].ansible_ssh_host
```

* * *

###### 排除指定的主机

```yaml
###########################################################
# ansible-playbook -i inventory.ini show-hostname-ip.yaml #
###########################################################

- hosts: etcd:!etcd[0]
  tasks:
    - name: 显示排除后的 inventory_hostname 与 IP
      debug:
        msg: "{{ inventory_hostname }} === {{ hostvars[inventory_hostname].ansible_ssh_host }}"

---

- hosts: etcd:!etcd[0]
  vars:
    IP: "{{ hostvars[groups.etcd[0]].ansible_ssh_host }}"
  tasks:
    - name: 只获取排除的 IP
      debug:
        msg: "{{ IP  }}"
```

* * *

* * *

* * *

###### 动态赋值变量

```yaml
##############################################
# ansible-playbook -i hosts.ini get-nic.yaml #
##############################################

- hosts: all
  gather_facts: false
  vars:
    # 相当于执行了这条命令： ls /etc/sysconfig/network-scripts/ifcfg-e* | grep -oE "[^-]+/?$"
    NIC: "{{ lookup('pipe', 'ls /etc/sysconfig/network-scripts/ifcfg-e*') | regex_search('[^-]+/?$') }}"
  tasks:
    - name: 动态获取主机网卡名
      debug:
        msg: "{{ NIC }}"

```

* * *

* * *

* * *

##### **注册**与**委托**

##### **`注册`**:

  **注册就是获取 shell命令执行后的`返回结果`**

* * *

###### 图解`注册`需求

**`如下需求 ansible-playbook 要如何实现`**

```ruby
                   +------->   master   由其中一台任意一台创建 master集群
                   |
  主控机 --+--------|------->   worker1   需要获取 master1中的jion命令，并加入集群
                   |
                   +------->   worker2   需要获取 master1中的jion命令，并加入集群
```

* * *

##### **`委托`**:

  **有三种关系， `主控、被控、委托`， 但我们只需要关注`代码在哪个主机上执行`即可** **主控**： 我们的`主控机` **被控**： `inventory.ini`中的 hosts **委托**： `delegate_to`指定的 hosts

| **主控机** | **程序执行的主机** |
| :-: | :-: |
| 默认 | `inventory.ini`中hosts的主机 |
| 委托 | `delegate_to`指定的hosts的主机 |

```yaml
# 添加 k8s worker 集群
- hosts: worker
  tags:
    - k8s
    - k8s-worker
  vars:
    IP: "{{ hostvars[groups.master[0]].ansible_ssh_host }}"
  tasks:

    - name: 获取k8s token
      # 将下面的命令委托给 master[0]主机来执行
      delegate_to: '{{ IP }}'
      # 明确指定ansible交互用户为 root，否则会使用当前用户
      remote_user: root
      shell: kubeadm token create --print-join-command
      # 保存shell执行的结果(得到加入k8s集群的命令)
      register: get_token

    - name: 添加k8s worker集群
      # 在非master[0]主机上，执行register中得到的命令
      shell: '{{ get_token.stdout }}'

```

* * *

* * *

* * *

###### 通过返回数字进行逻辑判断

```ruby
# 部署 master、worker 共同的配置
- hosts: containerd
  tags:
    - k8s
  tasks:

    - name: '检查镜像tar.gz是否存在'
      shell: find {{ deploy_dir }}/images/ -name k8s-{{K8sVersion}}.tar.gz | wc -l
      register: gz_exists

    - name: '解压镜像'
      shell: 'gzip -d {{ deploy_dir }}/images/k8s-{{K8sVersion}}.tar.gz'
      # 0：不存在;  >0 存在
      when:
        - gz_exists.stdout > '0'
```

* * *

* * *

* * *

###### 获取`inventory.ini`文件其它组中的内容

```yaml
###################################################
# ansible-playbook -i inventory.ini deploy.yaml #
###################################################

# 部署 HAProxy
- hosts: HAProxy
  tags:
    - haproxy
  tasks:
    - name: 修改配置文件
      blockinfile:
        path: /etc/haproxy/haproxy.cfg
        block: |-
          global
            maxconn 10000                 # 最大同时10000连接
            daemon                        # 以daemon方式在后台运行

          defaults
            log     127.0.0.1 local2      # local2 在 /etc/rsyslog.d/haproxy.conf 文件中配置
            # mode http                   # 默认的模式mode { tcp|http|health }，tcp是4层，http是7层，health只会返回OK
            retries         3             # 连接后端服务器失败重试次数，超过3次后会将失败的后端服务器标记为不可用。
            timeout client  1h            # 客户端响应超时             1小时
            timeout server  1h            # server端响应超时           1小时
            timeout connect 1h            # 连接server端超时           1小时
            timeout check   10s           # 对后端服务器的检测超时时间 10秒

          listen stats                    # 定义监控页面
            mode  http
            bind  *:1080                  # Web界面的1080端口
            stats refresh 1s              # 每1秒更新监控数据
            stats uri /stats              # 访问监控页面的uri
            stats realm HAProxy\ Stats    # 监控页面的认证提示
            stats auth admin:654321       # 监控页面的用户名和密码

          frontend kube_apiserver_front
            mode  tcp
            bind  *:6443                  # 监听6443端口
            default_backend kube_apiserver_back

          backend kube_apiserver_back

            mode    tcp
            option  tcp-check
            balance roundrobin
          # 我现在是在 HAProxy组下执行， 然后我要获取 master 组下的 IP地址
          {% for item in (groups.master) %}
          {{ '  server kube-apiserver-' ~loop.index~ ' ' ~hostvars[item].ansible_ssh_host~ ':6443 check inter 10s rise 3 fall 3 weight 1'}}
          {% endfor %}

        state: present
        create: yes
        backup: yes
        unsafe_writes: yes

```

* * *

* * *

* * *

###### 判断操作系统

```yaml
- hosts: servers
  tasks:

    - name: RedHat 关闭防火墙
      service:
        name: firewalld
        state: stopped
        enabled: no
      # 判断操作系统
      when:
        # ansible_os_family 是关键字可以直接判断
        - ansible_os_family == 'RedHat'

    - name: Debian 关闭防火墙
      service:
        name: ufw
        state: stopped
        enabled: no
      when:
        - ansible_os_family == 'Debian'
```

* * *

* * *

* * *

###### 获取本地主机IP地址

```yaml
## ansible-playbook debug.yaml

# 获取本地主机IP地址
- hosts: localhost
# 只链接本地
  connection: local
  tasks:
    - debug:
        # 获取所有 IP
        msg: "{{ ansible_all_ipv4_addresses }}"
    - debug:
        # 获取本机 IP
        msg: "{{ ansible_default_ipv4.address }}"

```

* * *

* * *

* * *

```yaml
- hosts: servers
  tasks:
    - name: 创建docker配置文件
      blockinfile:
        path: /etc/docker/daemon.json
        block: |-
          {
            "registry-mirrors": ["https://registry.cn-hangzhou.aliyuncs.com"],
            "exec-opts":["native.cgroupdriver=systemd"]
          }
        state: present
        create: yes
        backup: no
        unsafe_writes: yes
        mode: 0777
        # 去掉文件中的开始标记 # BEGIN ANSIBLE MANAGED BLOCK，结束标记 # END ANSIBLE MANAGED BLOCK
        marker: ""

```

* * *

* * *

* * *
