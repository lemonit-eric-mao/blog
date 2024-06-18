---
title: 'ansible-playbook 控制 kubeadm、etcdadm部署k8s 外部etcd'
date: '2020-08-20T13:12:45+00:00'
status: private
permalink: /2020/08/20/ansible-playbook-%e6%8e%a7%e5%88%b6-kubeadm%e3%80%81etcdadm%e9%83%a8%e7%bd%b2k8s-%e5%a4%96%e9%83%a8etcd
author: 毛巳煜
excerpt: ''
type: post
id: 5872
category:
    - Kubernetes
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
###### **[安装包](http://qiniu.dev-share.top/k8s-1.16.6-offline-setup-External-etcd.zip "安装包")**

- - - - - -

###### ansible.cfg

```ini
[defaults]

# 跳过 ssh 首次连接提示验证
host_key_checking = False

# 关闭警告提示
command_warnings = False

#
deprecation_warnings = False

# 执行任务的最大并发数
forks = 10

# 设置SSH链接超时时间
timeout = 1

# 统计任务处理时间
callback_whitelist = profile_tasks

# 收集Facts 并使用 Json文件存储
gather_facts = True
gathering = smart
fact_caching_timeout = 86400
fact_caching = jsonfile
fact_caching_connection = /tmp/cn_ansible_cache

;============================参数优化==========================

# 增加SSH连接保持时间为1天
[ssh_connection]
ssh_args = -o ControlMaster=auto -o ControlPersist=1d
pipelining = True


```

- - - - - -

###### hosts.ini

```ini
# 根据实际情况，分配主机
[servers]
haproxy01       ansible_ssh_host=192.168.20.78
haproxy02       ansible_ssh_host=192.168.20.79
master01        ansible_ssh_host=192.168.20.81
master02        ansible_ssh_host=192.168.20.82
master03        ansible_ssh_host=192.168.20.83
worker01        ansible_ssh_host=192.168.20.84
worker02        ansible_ssh_host=192.168.20.85
worker03        ansible_ssh_host=192.168.20.86
etcd01          ansible_ssh_host=192.168.20.87
etcd02          ansible_ssh_host=192.168.20.88
etcd03          ansible_ssh_host=192.168.20.89


[all:vars]
username = root
# 主控机存放源文件的目录
src_file_dir= /home/deploy/src_file_dir
# 指定程序安装目录
deploy_dir = /home/deploy/offline_setup
# 时间同步服务器
ntp_server = pool.ntp.org


```

- - - - - -

###### inventory.ini

```ini
# 所有主机IP地址
[servers]
192.168.20.78
192.168.20.79
192.168.20.81
192.168.20.82
192.168.20.83
192.168.20.84
192.168.20.85
192.168.20.86
192.168.20.87
192.168.20.88
192.168.20.89

# HAProxy提供高可用，如果不需要，至少保留一台 HAProxy主机
[HAProxy]
haproxy01 ansible_ssh_host=192.168.20.78
haproxy02 ansible_ssh_host=192.168.20.79

# HAProxy提供高可用，如果不需要高可用，不输入即可
[KeepAlived]
KeepAlived1 ansible_ssh_host=192.168.20.78
KeepAlived2 ansible_ssh_host=192.168.20.79

# 指定需要安装docker的主机
[docker]
master01 ansible_ssh_host=192.168.20.81
master02 ansible_ssh_host=192.168.20.82
master03 ansible_ssh_host=192.168.20.83
worker01 ansible_ssh_host=192.168.20.84
worker02 ansible_ssh_host=192.168.20.85
worker03 ansible_ssh_host=192.168.20.86

# 指定master主机，至少3台
[master]
master01 ansible_ssh_host=192.168.20.81
master02 ansible_ssh_host=192.168.20.82
master03 ansible_ssh_host=192.168.20.83

# 指定worker主机
[worker]
worker01 ansible_ssh_host=192.168.20.84
worker02 ansible_ssh_host=192.168.20.85
worker03 ansible_ssh_host=192.168.20.86

# etcd 部署到哪些主机，至少3台
[etcd]
etcd01 ansible_ssh_host=192.168.20.87
etcd02 ansible_ssh_host=192.168.20.88
etcd03 ansible_ssh_host=192.168.20.89


[all:vars]
username = root
# 指定程序安装目录
deploy_dir = /home/deploy/offline_setup
# 设置虚IP，如果没有虚IP这里设置 HAProxy的IP
VirtualIP = 192.168.20.76
# k8s 版本
K8sVersion = 1.16.6
# 因为是外部部署etcd，这里要指定etcd的版本
etcd_version = 3.3.8


```

- - - - - -

###### 1\_init.yaml

```yaml
########################################################
# ansible-playbook -i hosts.ini 1_init.yaml -u root -k #
########################################################

- hosts: servers
  tasks:
    - name: 建立SSH互信
      authorized_key:
        user: "{{ username }}"
        key: "{{ lookup('file', lookup('env','HOME')+ '/.ssh/id_rsa.pub') }}"
        state: present

    - name: 设置hostame
      shell: hostnamectl set-hostname {{ inventory_hostname }}

    - name: 添加 hosts
      blockinfile:
        path: /etc/hosts
        block: |-
          {% for item in (groups.servers) %}
          {{ hostvars[item].ansible_ssh_host }}  {{ item }}
          {% endfor %}
        state: present
        create: yes
        backup: yes
        unsafe_writes: yes

    - name: SSH连接加速
      shell: sed -i 's/\#UseDNS yes/UseDNS no/g' /etc/ssh/sshd_config && systemctl restart sshd

    - name: 构建目录
      file:
        path: '{{ deploy_dir }}'
        state: directory

    - name: 关闭防火墙
      service:
        name: firewalld
        state: stopped
        enabled: no

    - name: 关闭SELinux
      lineinfile:
        dest: '/etc/selinux/config'
        line: 'SELINUX=permissive'
        regexp: 'SELINUX=enforcing'
        state: present

    - name: 关闭Swap
      shell: swapoff -a && sed -ri 's/.*swap.*/#&/' /etc/fstab && systemctl daemon-reload


```

- - - - - -

###### 2\_deploy\_ntp.yaml

```yaml
###################################################
# ansible-playbook -i hosts.ini 2_deploy_ntp.yaml #
###################################################

- hosts: all
  tasks:
    - name: get facts
      setup:

    - name: '将本地文件拷贝至各主机'
      copy:
        src: '../rpm-lib/ntp'
        dest: '{{ deploy_dir }}/rpm-lib/'

    - name: '离线安装NTP客户端'
      shell: rpm -ivh {{ deploy_dir }}/rpm-lib/ntp/* --force --nodeps

    - name: 删除配置文件
      file:
        path: /etc/ntp.conf
        state: absent

    - name: 新增配置文件
      blockinfile:
        path: /etc/ntp.conf
        block: |-

          driftfile /var/lib/ntp/drift
          #
          restrict default nomodify notrap nopeer noquery
          #
          restrict 127.0.0.1
          restrict ::1
          # 日志目录.
          logfile /var/log/ntpd.log
          # 设置时间同步服务器
          server {{ ntp_server }}
          #
          includefile /etc/ntp/crypto/pw
          #
          keys /etc/ntp/keys
          #
          disable monitor

        state: present
        create: yes
        backup: no
        unsafe_writes: yes

    - name: 启动 ntpd 自动同步
      service:
        name: ntpd
        state: started
        enabled: yes


```

- - - - - -

###### 3\_deploy\_docker.yaml

```yaml
##########################################################
# ansible-playbook -i inventory.ini 3_deploy_docker.yaml #
##########################################################

# 部署 docker
- hosts: docker
  tags:
    - docker
  tasks:

    - name: '检查Docker是否存在'
      shell: find /usr/lib/systemd/system/ -name docker.service | wc -l
      register: exists

    - name: '将本地文件拷贝至各主机'
      copy:
        src: '../rpm-lib/docker'
        dest: '{{ deploy_dir }}/rpm-lib/'
      # 0：不存在;  >0 存在
      when:
        - exists.stdout == '0'

    - name: 离线安装 docker
      shell: rpm -ivh {{ deploy_dir }}/rpm-lib/docker/* --force --nodeps
      # 0：不存在;  >0 存在
      when:
        - exists.stdout == '0'

    - name: 启动 docker
      service:
        name: docker
        state: started
        enabled: yes
      # 0：不存在;  >0 存在
      when:
        - exists.stdout == '0'


```

- - - - - -

###### 4\_deploy.yaml

```yaml
###################################################
# ansible-playbook -i inventory.ini 4_deploy.yaml #
###################################################

# 部署 tools
- hosts: servers
  tags:
    - tools
  tasks:
    - name: '将本地文件拷贝至各主机'
      copy:
        src: '../rpm-lib/tools'
        dest: '{{ deploy_dir }}/rpm-lib/'

    - name: 安装工具
      shell: rpm -ivh {{ deploy_dir }}/rpm-lib/tools/* --force --nodeps

    - name: 删除安装包
      shell: rm -rf {{ deploy_dir }}/rpm-lib/tools


# 部署 HAProxy
- hosts: HAProxy
  tags:
    - haproxy
  tasks:
    - name: '将本地文件拷贝至各主机'
      copy:
        src: '../rpm-lib/haproxy'
        dest: '{{ deploy_dir }}/rpm-lib/'

    - name: '离线安装 haproxy'
      shell: rpm -ivh {{ deploy_dir }}/rpm-lib/haproxy/* --force --nodeps

    - name: 配置日志
      shell: echo 'local2=debug     /var/log/haproxy.log' > /etc/rsyslog.d/haproxy.conf && systemctl restart rsyslog

    - name: 删除文件
      file:
        path: /etc/haproxy/haproxy.cfg
        state: absent

    - name: 修改配置文件
      blockinfile:
        path: /etc/haproxy/haproxy.cfg
        block: |-
          global
            maxconn 10000
            daemon

          defaults
            log     127.0.0.1 local2
            retries         3
            timeout client  1h
            timeout server  1h
            timeout connect 1h
            timeout check   10s

          listen stats
            mode  http
            bind  *:1080
            stats refresh 1s
            stats uri /stats
            stats realm HAProxy\ Stats
            stats auth admin:654321

          frontend kube_apiserver_front
            mode  tcp
            bind  *:6443
            default_backend kube_apiserver_back

          backend kube_apiserver_back

            mode    tcp
            option  tcp-check
            balance roundrobin

          {% for item in (groups.master) %}
          {{ '  server kube-apiserver-' ~loop.index~ ' ' ~hostvars[item].ansible_ssh_host~ ':6443 check inter 10s rise 3 fall 3 weight 1' }}
          {% endfor %}

        state: present
        create: yes
        backup: no
        unsafe_writes: yes



# 部署 KeepAlived 主
- hosts: KeepAlived[0]
  tags:
    - keepalived
    - keepalived-master
  vars:
    NIC: "{{ lookup('pipe', 'ls /etc/sysconfig/network-scripts/ifcfg-e*') | regex_search('[^-]+/?<span class="katex math inline">') }}"
  tasks:
    - name: '将本地文件拷贝至各主机'
      copy:
        src: '../rpm-lib/keepalived'
        dest: '{{ deploy_dir }}/rpm-lib/'

    - name: '离线安装 keepalived'
      shell: rpm -ivh {{ deploy_dir }}/rpm-lib/keepalived/* --force --nodeps

    - name: 删除文件
      file:
        path: /etc/keepalived/scripts/check_haproxy.sh
        state: absent

    - name: 创建检测脚本
      blockinfile:
        path: /etc/keepalived/scripts/check_haproxy.sh
        block: |-
          #!/bin/bash
          line=</span>(netstat -lntp | grep 6443 | wc -l)
          if [ "<span class="katex math inline">{line}" = "0" ]; then
               systemctl stop keepalived
          fi
        state: present
        create: yes
        backup: no
        unsafe_writes: yes
        mode: 0777

    - name: 删除文件
      file:
        path: /etc/keepalived/keepalived.conf
        state: absent

    - name: 修改配置文件
      blockinfile:
        path: /etc/keepalived/keepalived.conf
        block: |-
          global_defs {
             notification_email {
               eric.mao@sinoeyes.com
             }
             notification_email_from eric@qq.com
             smtp_server smtp.exmail.qq.com
             smtp_connect_timeout 30
             router_id eric_keepalived_master
             vrrp_skip_check_adv_addr
             vrrp_garp_interval 0
             vrrp_gna_interval 0
          }
          vrrp_script check_haproxy {
              script "/etc/keepalived/scripts/check_haproxy.sh"
              interval 1
              weight 2
          }
          vrrp_instance ERIC_VI_1 {

              nopreempt
              state MASTER
              virtual_router_id 56
              priority 160
              advert_int 1
              authentication {
                  auth_type PASS
                  auth_pass 1111
              }
              interface {{ NIC }}
              virtual_ipaddress {
                  {{ VirtualIP }}/24
              }
              track_script {
                  check_haproxy
              }
          }

        state: present
        create: yes
        backup: no
        unsafe_writes: yes
        mode: 0644


# 部署 KeepAlived 备用
- hosts: KeepAlived:!KeepAlived[0]
  tags:
    - keepalived
    - keepalived-backup
  vars:
    NIC: "{{ lookup('pipe', 'ls /etc/sysconfig/network-scripts/ifcfg-e*') | regex_search('[^-]+/?</span>') }}"
  tasks:
    - name: '将本地文件拷贝至各主机'
      copy:
        src: '../rpm-lib/keepalived'
        dest: '{{ deploy_dir }}/rpm-lib/'

    - name: '离线安装 keepalived'
      shell: rpm -ivh {{ deploy_dir }}/rpm-lib/keepalived/* --force --nodeps

    - name: 删除文件
      file:
        path: /etc/keepalived/scripts/check_haproxy.sh
        state: absent

    - name: 创建检测脚本
      blockinfile:
        path: /etc/keepalived/scripts/check_haproxy.sh
        block: |-
          #!/bin/bash
          line=<span class="katex math inline">(netstat -lntp | grep 6443 | wc -l)
          if [ "</span>{line}" = "0" ]; then
               systemctl stop keepalived
          fi
        state: present
        create: yes
        backup: no
        unsafe_writes: yes
        mode: 0777

    - name: 删除文件
      file:
        path: /etc/keepalived/keepalived.conf
        state: absent

    - name: 修改配置文件
      blockinfile:
        path: /etc/keepalived/keepalived.conf
        block: |-

          # 1 全局块
          global_defs {
             notification_email {
               eric.mao@sinoeyes.com
             }
             notification_email_from eric@qq.com
             smtp_server smtp.exmail.qq.com
             smtp_connect_timeout 30
             router_id eric_keepalived_master
             vrrp_skip_check_adv_addr
             vrrp_garp_interval 0
             vrrp_gna_interval 0
          }
          vrrp_script check_haproxy {
              script "/etc/keepalived/scripts/check_haproxy.sh"
              interval 1
              weight 2
          }
          vrrp_instance ERIC_VI_1 {

              nopreempt
              state BACKUP
              virtual_router_id 56
              priority 100
              advert_int 1
              authentication {
                  auth_type PASS
                  auth_pass 1111
              }
              interface {{ NIC }}
              virtual_ipaddress {
                  {{ VirtualIP }}/24
              }
              track_script {
                  check_haproxy
              }
          }

        state: present
        create: yes
        backup: no
        unsafe_writes: yes
        mode: 0644


# 部署 etcd
- hosts: etcd
  tags:
    - etcd
  tasks:
    - name: 离线安装 etcdadm
      copy:
        src: '../etcd/etcdadm'
        dest: '/usr/local/bin/'
        mode: 0777

    - name: create a file
      file:
        path: '/var/cache/etcdadm/etcd/v{{ etcd_version }}'
        state: directory

    - name: '将本地文件拷贝至各主机'
      copy:
        src: '../etcd/etcd-v{{ etcd_version }}-linux-amd64.tar.gz'
        dest: '/var/cache/etcdadm/etcd/v{{ etcd_version }}'


# 部署 master、worker 共同的配置
- hosts: docker
  tags:
    - k8s
  tasks:
    - name: '将本地kubeadm|kubelet|kubectl文件拷贝至各主机'
      copy:
        src: '../rpm-lib/k8s'
        dest: '{{ deploy_dir }}/rpm-lib/'

    - name: 离线安装 kubeadm|kubelet|kubectl
      shell: rpm -ivh {{ deploy_dir }}/rpm-lib/k8s/* --force --nodeps

    - name: kubelet 开机自启动
      shell: systemctl enable kubelet

    - name: 创建k8s.conf文件
      # 创建文件
      file:
        path: '/etc/sysctl.d/k8s.conf'
        state: touch
        owner: root
        group:  root

    - name: 新增/替换 多条文件内容
      lineinfile:
        dest: '/etc/sysctl.d/k8s.conf'
        line: '{{ item.key }} = {{ item.value }}'
        regexp: '^{{ item.key }}.*'
        state: present
      with_items:
        - { key: "net.bridge.bridge-nf-call-ip6tables", value: "1" }
        - { key: "net.bridge.bridge-nf-call-iptables", value: "1" }

    - name: 更新配置
      shell: 'sysctl -p /etc/sysctl.d/k8s.conf && sysctl --system && echo 1 > /proc/sys/net/bridge/bridge-nf-call-iptables && echo "KUBELET_EXTRA_ARGS=--fail-swap-on=false" > /etc/sysconfig/kubelet'

    - name: '检查镜像是否存在'
      shell: find {{ deploy_dir }}/images/ -name k8s-{{ K8sVersion }}.docker | wc -l
      register: exists

    - name: '将本地镜像文件拷贝至各主机'
      copy:
        src: '../images'
        dest: '{{ deploy_dir }}/'
      # 0：不存在;  >0 存在
      when:
        - exists.stdout == '0'

    - name: 加载镜像
      shell: 'docker load 
```

- - - - - -

###### 5\_start.yaml

```yaml
##################################################
# ansible-playbook -i inventory.ini 5_start.yaml #
##################################################

# 启动 HAProxy
- hosts: HAProxy
  tags:
    - haproxy
  tasks:
    - name: '启动 HAProxy'
      service:
        name: haproxy
        state: started
        enabled: yes


# 启动 Keepalived
- hosts: KeepAlived
  tags:
    - keepalived
  tasks:
    - name: 启动 KeepAlived
      service:
        name: keepalived
        state: started
        enabled: yes


# 初始化 etcd[0]
- hosts: etcd[0]
  tags:
    - etcd
    - etcd-init
  tasks:
    - name: 初始化 etcd
      shell: 'etcdadm init'

    - name: 将证书拉到主控机
      fetch:
        src: '/etc/etcd/pki/{{ item }}'
        dest: '/etc/etcd/pki/'
        flat: 'yes'
      loop:
        - apiserver-etcd-client.crt
        - apiserver-etcd-client.key
        - ca.crt
        - ca.key
        - etcdctl-etcd-client.crt
        - etcdctl-etcd-client.key
        - peer.crt
        - peer.key
        - server.crt
        - server.key


# 加入etcd集群
- hosts: etcd:!etcd[0]
  tags:
    - etcd
    - etcd-join
  vars:
    IP: "{{ hostvars[groups.etcd[0]].ansible_ssh_host }}"
  tasks:
    - name: 推送证书到其它etcd主机
      copy:
        src: '/etc/etcd/pki/{{ item }}'
        dest: '/etc/etcd/pki/'
      loop:
        - ca.crt
        - ca.key

    - name: 加入到etcd集群
      shell: 'etcdadm join https://{{ IP }}:2379'


# 将etcd证书推送到所有k8s-master主机
- hosts: master
  tags:
    - k8s
    - k8s-etcd-pki
  tasks:
    - name: 将etcd证书推送到所有k8s-master主机
      copy:
        src: '/etc/etcd/pki'
        dest: '/etc/etcd/'


# 初始化 k8s master[0]
- hosts: master[0]
  tags:
    - k8s
    - k8s-init
  tasks:
    - name: 初始化 k8s-master
      shell: 'kubeadm init --config={{ deploy_dir }}/yaml/kubeadm-init.yaml'

    - name: 创建文件夹
      shell: '{{ item }}'
      loop:
        - mkdir -p <span class="katex math inline">HOME/.kube
        - cp -i /etc/kubernetes/admin.conf</span>HOME/.kube/config
        - chown <span class="katex math inline">(id -u):</span>(id -g) <span class="katex math inline">HOME/.kube/config

    - name: 加入网络插件
      shell: 'kubectl apply -f {{ deploy_dir }}/yaml/canal.yaml'

    - name: 将证书拉到主控机
      fetch:
        src: '/etc/kubernetes/pki/{{ item }}'
        dest: '/etc/kubernetes/pki/'
        flat: 'yes'
      loop:
        - ca.crt
        - ca.key
        - front-proxy-ca.crt
        - front-proxy-ca.key
        - front-proxy-client.crt
        - front-proxy-client.key
        - sa.key
        - sa.pub


# 加入 k8s master 集群
- hosts: master:!master[0]
  tags:
    - k8s
    - k8s-master
  vars:
    IP: "{{ hostvars[groups.master[0]].ansible_ssh_host }}"
  tasks:
    - name: 推送证书到其它k8s master主机
      copy:
        src: '/etc/kubernetes/pki'
        dest: '/etc/kubernetes/'

    - name: 获取k8s token
      delegate_to: '{{ IP }}'
      remote_user: root
      shell: kubeadm token create --print-join-command
      register: get_token

    - name: 加入到k8s master集群
      shell: '{{ get_token.stdout }} --control-plane'

    - name: 创建文件夹
      shell: '{{ item }}'
      loop:
        - mkdir -p</span>HOME/.kube
        - cp -i /etc/kubernetes/admin.conf <span class="katex math inline">HOME/.kube/config
        - chown</span>(id -u):<span class="katex math inline">(id -g)</span>HOME/.kube/config


# 添加 k8s worker 集群
- hosts: worker
  tags:
    - k8s
    - k8s-worker
  vars:
    IP: "{{ hostvars[groups.master[0]].ansible_ssh_host }}"
  tasks:
    - name: 获取k8s token
      delegate_to: '{{ IP }}'
      shell: kubeadm token create --print-join-command
      register: get_token

    - name: 添加k8s worker集群
      shell: '{{ get_token.stdout }}'


```

- - - - - -

###### 6\_stop.yaml

```yaml
#################################################
# ansible-playbook -i inventory.ini 6_stop.yaml #
#################################################

# 停止 HAProxy
- hosts: HAProxy
  gather_facts: false
  tags:
    - haproxy
  tasks:
    - name: '停止 HAProxy'
      ignore_errors: yes
      service:
        name: haproxy
        state: stopped
        enabled: no


# 停止 Keepalived
- hosts: KeepAlived
  tags:
    - keepalived
  tasks:
    - name: 停止 KeepAlived
      ignore_errors: yes
      service:
        name: keepalived
        state: stopped
        enabled: no


```

- - - - - -

###### 7\_destory.yaml

```yaml
####################################################
# ansible-playbook -i inventory.ini 7_destory.yaml #
####################################################

- hosts: localhost
  gather_facts: false
  tasks:
    - name: confirm operation
      pause:
        prompt: "该操作将清除群集, 并且数据将被删除(中止：Ctrl-c 输入A, 继续: Ctrl-c 输入C, 或直接回车)"

- import_playbook: 6_stop.yaml


# 清除 HAProxy
- hosts: HAProxy
  tags:
    - haproxy
  tasks:
    - name: 清除资源
      ignore_errors: yes
      shell: "{{ item }}"
      loop:
        - yum -y remove haproxy
        - rm -rf {{ deploy_dir }}
        - rm -rf /etc/haproxy/
        - rm -rf /etc/rsyslog.d/haproxy.conf
        - systemctl restart rsyslog


# 清除 Keepalived
- hosts: KeepAlived
  tags:
    - keepalived
  tasks:
    - name: 清除资源
      ignore_errors: yes
      shell: "{{ item }}"
      loop:
        - yum -y remove keepalived
        - rm -rf {{ deploy_dir }}
        - rm -rf /etc/keepalived/scripts/check_haproxy.sh
        - rm -rf /etc/keepalived/keepalived.conf


# 清除 etcd
- hosts: etcd
  tags:
    - etcd
  tasks:
    - name: 重置 etcd
      shell: etcdadm reset

    - name: 清除资源
      ignore_errors: yes
      shell: "{{ item }}"
      loop:
        - rm -rf /usr/local/bin/etcdadm
        - rm -rf /var/cache/etcdadm/
        - rm -rf {{ deploy_dir }}


# 清除 k8s
- hosts: docker
  tags:
    - k8s
  tasks:
    - name: 清除 k8s
      ignore_errors: yes
      shell: "{{ item }}"
      loop:
        - kubeadm reset -f
        - rm -rf ~/.kube/
        - systemctl stop kubelet
        - yum -y remove kubelet kubeadm kubectl
        - systemctl daemon-reload
        - modprobe -r ipip
        - rm -rf /etc/kubernetes/
        - rm -rf /etc/systemd/system/kubelet.service.d
        - rm -rf /etc/systemd/system/kubelet.service
        - rm -rf /usr/bin/kube*
        - rm -rf /etc/cni
        - rm -rf /opt/cni


```

- - - - - -

###### setup.sh

```shell
#! /usr/bin/bash

set -e
cd <span class="katex math inline">(cd `dirname</span>0`; pwd)

# ========================================================================

# 设定命令菜单
declare -A map=()
map['0']="ansible-playbook -i hosts.ini yaml/1_init.yaml -u root -k"
map['1']="ansible-playbook -i hosts.ini yaml/2_deploy_ntp.yaml"
map['2']="ansible-playbook -i inventory.ini yaml/3_deploy_docker.yaml"
map['3']="ansible-playbook -i inventory.ini yaml/4_deploy.yaml"
map['4']="ansible-playbook -i inventory.ini yaml/5_start.yaml"

# 设定提示菜单
declare -A menu=()
menu[0]='初始化各主机'
menu[1]='同步ntp'
menu[2]='部署docker'
menu[3]='部署k8s'
menu[4]='启动k8s'
menu[5]='开始执行'

# 选择的命令集
declare -A cmds=()


echo -e "\033[36m +------------------------------------------+ \033[0m"
echo -e "\033[36m |         请选择要执行的步骤\033[0m \033[33m(多选) \033[0m \033[36m      | \033[0m"
echo -e "\033[36m +------------------------------------------+ \033[0m"


select val in <span class="katex math inline">{menu[@]}
do
    echo -e "\033[36m</span>val: \033[0m"
    case "<span class="katex math inline">val" in
        初始化各主机)
            cmds[</span>{#cmds[@]}]=0
        ;;

        同步ntp)
            cmds[<span class="katex math inline">{#cmds[@]}]=1
        ;;

        部署docker)
            cmds[</span>{#cmds[@]}]=2
        ;;

        部署k8s)
            cmds[<span class="katex math inline">{#cmds[@]}]=3
        ;;

        启动k8s)
            cmds[</span>{#cmds[@]}]=4
        ;;

        开始执行)
            break
        ;;

        *)
            echo -e "\033[31m 输入错误，程序退出 \033[0m"
            exit
        ;;
    esac
done

start_time=`date +'%Y-%m-%d %H:%M:%S'`
start_seconds=<span class="katex math inline">(date --date="</span>start_time" +%s)

# shell 排序去重数组
new_cmds=(<span class="katex math inline">(echo</span>{cmds[@]} | sed 's/ /\n/g'| sort | uniq))

# 批量执行
for i in <span class="katex math inline">{new_cmds[@]}
do</span>{map[<span class="katex math inline">i]}
done

# ========================================================================
end_time=`date +'%Y-%m-%d %H:%M:%S'`
end_seconds=</span>(date --date="<span class="katex math inline">end_time" +%s)
echo  -e "\033[36m ==========================脚本执行时间：</span>[<span class="katex math inline">end_seconds -</span>start_seconds]秒============================== \033[0m"


```

- - - - - -

- - - - - -

- - - - - -