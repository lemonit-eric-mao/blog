---
title: "ansible-playbook 控制 kubeadm部署k8s 堆叠etcd"
date: "2020-08-24"
categories: 
  - "k8s"
---

###### **[安装包](http://qiniu.dev-share.top/k8s-1.16.6-offline-setup-Stacking-etcd.zip "安装包")** 压缩包密码是自己常用密码

* * *

###### 目录

```ruby
[root@Control ~]# tree /home/deploy/offline_setup/
/home/deploy/offline_setup/
├── ansible.cfg
├── hosts.ini
├── setup.sh
├── inventory.ini
├── images
│   ├── calico-cni-v3.15.1.docker
│   ├── calico-node-v3.15.1.docker
│   ├── calico-pod2daemon-flexvol-v3.15.1.docker
│   ├── calico-kube-controllers-v3.15.1.docker
│   ├── flanneld-v0.11.0-amd64.docker
│   ├── k8s.gcr.io-coredns-1.6.2.docker
│   ├── k8s.gcr.io-kube-apiserver-v1.16.6.docker
│   ├── k8s.gcr.io-kube-controller-manager-v1.16.6.docker
│   ├── k8s.gcr.io-kube-proxy-v1.16.6.docker
│   ├── k8s.gcr.io-kube-scheduler-v1.16.6.docker
│   ├── k8s.gcr.io-etcd-3.3.15-0.docker
│   └── k8s.gcr.io-pause-3.1.docker
├── rpm-lib
│   ├── ansible
│   │   ├── ansible-2.9.10-1.el7.noarch.rpm
│   │   ├── libyaml-0.1.4-11.el7_0.x86_64.rpm
│   │   ├── python2-cryptography-1.7.2-2.el7.x86_64.rpm
│   │   ├── python2-httplib2-0.18.1-3.el7.noarch.rpm
│   │   ├── python2-jmespath-0.9.4-2.el7.noarch.rpm
│   │   ├── python2-pyasn1-0.1.9-7.el7.noarch.rpm
│   │   ├── python-babel-0.9.6-8.el7.noarch.rpm
│   │   ├── python-backports-1.0-8.el7.x86_64.rpm
│   │   ├── python-backports-ssl_match_hostname-3.5.0.1-1.el7.noarch.rpm
│   │   ├── python-cffi-1.6.0-5.el7.x86_64.rpm
│   │   ├── python-enum34-1.0.4-1.el7.noarch.rpm
│   │   ├── python-idna-2.4-1.el7.noarch.rpm
│   │   ├── python-ipaddress-1.0.16-2.el7.noarch.rpm
│   │   ├── python-jinja2-2.7.2-4.el7.noarch.rpm
│   │   ├── python-markupsafe-0.11-10.el7.x86_64.rpm
│   │   ├── python-paramiko-2.1.1-9.el7.noarch.rpm
│   │   ├── python-ply-3.4-11.el7.noarch.rpm
│   │   ├── python-pycparser-2.14-1.el7.noarch.rpm
│   │   ├── python-setuptools-0.9.8-7.el7.noarch.rpm
│   │   ├── python-six-1.9.0-2.el7.noarch.rpm
│   │   ├── PyYAML-3.10-11.el7.x86_64.rpm
│   │   └── sshpass-1.06-2.el7.x86_64.rpm
│   ├── docker
│   │   ├── audit-2.8.5-4.el7.x86_64.rpm
│   │   ├── audit-libs-2.8.5-4.el7.x86_64.rpm
│   │   ├── audit-libs-python-2.8.5-4.el7.x86_64.rpm
│   │   ├── checkpolicy-2.5-8.el7.x86_64.rpm
│   │   ├── containerd.io-1.2.13-3.2.el7.x86_64.rpm
│   │   ├── container-selinux-2.119.2-1.911c772.el7_8.noarch.rpm
│   │   ├── docker-ce-19.03.9-3.el7.x86_64.rpm
│   │   ├── docker-ce-cli-19.03.12-3.el7.x86_64.rpm
│   │   ├── libcgroup-0.41-21.el7.x86_64.rpm
│   │   ├── libseccomp-2.3.1-4.el7.x86_64.rpm
│   │   ├── libsemanage-python-2.5-14.el7.x86_64.rpm
│   │   ├── policycoreutils-2.5-34.el7.x86_64.rpm
│   │   ├── policycoreutils-python-2.5-34.el7.x86_64.rpm
│   │   ├── python-IPy-0.75-6.el7.noarch.rpm
│   │   └── setools-libs-3.3.8-4.el7.x86_64.rpm
│   ├── haproxy
│   │   ├── haproxy22-2.2.1-1.el7.ius.x86_64.rpm
│   │   └── pcre2-10.23-2.el7.x86_64.rpm
│   ├── k8s
│   │   ├── 029bc0d7b2112098bdfa3f4621f2ce325d7a2c336f98fa80395a3a112ab2a713-kubernetes-cni-0.8.6-0.x86_64.rpm
│   │   ├── 0bfd3f23e53d4663860cd89b9304fba5a7853d7b02a8985e4d3c240d10bf6587-kubectl-1.16.6-0.x86_64.rpm
│   │   ├── 0eeb459890b1c8f07c91a9771ce5f4df6c2b318ff2e8902ed9228bf01944cfd7-kubeadm-1.16.6-0.x86_64.rpm
│   │   └── 6f0d57f3271c856b9790f6628d0fa2f2d51e5e5c33faf2d826f3fc07a1907cde-kubelet-1.16.6-0.x86_64.rpm
│   ├── keepalived
│   │   ├── keepalived-1.3.5-16.el7.x86_64.rpm
│   │   ├── lm_sensors-libs-3.4.0-8.20160601gitf9185e5.el7.x86_64.rpm
│   │   ├── net-snmp-agent-libs-5.7.2-48.el7_8.1.x86_64.rpm
│   │   └── net-snmp-libs-5.7.2-48.el7_8.1.x86_64.rpm
│   ├── ntp
│   │   ├── autogen-libopts-5.18-5.el7.x86_64.rpm
│   │   ├── ntp-4.2.6p5-29.el7.centos.2.x86_64.rpm
│   │   └── ntpdate-4.2.6p5-29.el7.centos.2.x86_64.rpm
│   └── tools
│       ├── gpm-libs-1.20.7-6.el7.x86_64.rpm
│       ├── net-tools-2.0-0.25.20131004git.el7.x86_64.rpm
│       ├── perl-5.16.3-295.el7.x86_64.rpm
│       ├── perl-Carp-1.26-244.el7.noarch.rpm
│       ├── perl-constant-1.27-2.el7.noarch.rpm
│       ├── perl-Encode-2.51-7.el7.x86_64.rpm
│       ├── perl-Exporter-5.68-3.el7.noarch.rpm
│       ├── perl-File-Path-2.09-2.el7.noarch.rpm
│       ├── perl-File-Temp-0.23.01-3.el7.noarch.rpm
│       ├── perl-Filter-1.49-3.el7.x86_64.rpm
│       ├── perl-Getopt-Long-2.40-3.el7.noarch.rpm
│       ├── perl-HTTP-Tiny-0.033-3.el7.noarch.rpm
│       ├── perl-libs-5.16.3-295.el7.x86_64.rpm
│       ├── perl-macros-5.16.3-295.el7.x86_64.rpm
│       ├── perl-parent-0.225-244.el7.noarch.rpm
│       ├── perl-PathTools-3.40-5.el7.x86_64.rpm
│       ├── perl-Pod-Escapes-1.04-295.el7.noarch.rpm
│       ├── perl-podlators-2.5.1-3.el7.noarch.rpm
│       ├── perl-Pod-Perldoc-3.20-4.el7.noarch.rpm
│       ├── perl-Pod-Simple-3.28-4.el7.noarch.rpm
│       ├── perl-Pod-Usage-1.63-3.el7.noarch.rpm
│       ├── perl-Scalar-List-Utils-1.27-248.el7.x86_64.rpm
│       ├── perl-Socket-2.010-5.el7.x86_64.rpm
│       ├── perl-Storable-2.45-3.el7.x86_64.rpm
│       ├── perl-Text-ParseWords-3.29-4.el7.noarch.rpm
│       ├── perl-threads-1.87-4.el7.x86_64.rpm
│       ├── perl-threads-shared-1.43-6.el7.x86_64.rpm
│       ├── perl-Time-HiRes-1.9725-3.el7.x86_64.rpm
│       ├── perl-Time-Local-1.2300-2.el7.noarch.rpm
│       ├── vim-common-7.4.629-6.el7.x86_64.rpm
│       ├── vim-enhanced-7.4.629-6.el7.x86_64.rpm
│       └── vim-filesystem-7.4.629-6.el7.x86_64.rpm
└── yaml
    ├── 1_init.yaml
    ├── 2_deploy_ntp.yaml
    ├── 3_deploy_docker.yaml
    ├── 4_deploy.yaml
    ├── 5_start.yaml
    ├── 6_stop.yaml
    ├── 7_destory.yaml
    └── canal.yaml
```

* * *

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

* * *

###### hosts.ini

```ini
# 根据实际情况，分配主机
[servers]
HAProxy1      ansible_ssh_host=192.168.20.78
HAProxy2      ansible_ssh_host=192.168.20.79
master01      ansible_ssh_host=192.168.20.81
master02      ansible_ssh_host=192.168.20.82
master03      ansible_ssh_host=192.168.20.83
worker01      ansible_ssh_host=192.168.20.84
worker02      ansible_ssh_host=192.168.20.85
worker03      ansible_ssh_host=192.168.20.86


[all:vars]
username = root
# 主控机存放源文件的目录
src_file_dir= /home/deploy/src_file_dir
# 指定程序安装目录
deploy_dir = /home/deploy/offline_setup
# 指定时间同步服务器
ntp_server = pool.ntp.org
```

* * *

###### **`注：`** 如果想改为单 HAProxy 模式时，需要修改 `inventory.ini`文件如下

1 只需要保留一个HAProxy的IP地址 2 去掉KeepAlived下的所有IP 3 将 文件中的 VirtualIP 设置为HAProxy的IP地址

* * *

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

# HAProxy提供高可用，如果不需要，至少保留一台 HAProxy主机
[HAProxy]
HAProxy1      ansible_ssh_host=192.168.20.78
HAProxy2      ansible_ssh_host=192.168.20.79

# HAProxy提供高可用，如果不需要高可用，不输入即可
[KeepAlived]
KeepAlived1   ansible_ssh_host=192.168.20.78
KeepAlived2   ansible_ssh_host=192.168.20.79

# 指定需要安装docker的主机
[docker]
master01      ansible_ssh_host=192.168.20.81
master02      ansible_ssh_host=192.168.20.82
master03      ansible_ssh_host=192.168.20.83
worker01      ansible_ssh_host=192.168.20.84
worker02      ansible_ssh_host=192.168.20.85
worker03      ansible_ssh_host=192.168.20.86

# 指定master主机，至少3台
[master]
master01      ansible_ssh_host=192.168.20.81
master02      ansible_ssh_host=192.168.20.82
master03      ansible_ssh_host=192.168.20.83

# 指定worker主机
[worker]
worker01      ansible_ssh_host=192.168.20.84
worker02      ansible_ssh_host=192.168.20.85
worker03      ansible_ssh_host=192.168.20.86


[all:vars]
username = root
# 指定程序安装目录
deploy_dir = /home/deploy/offline_setup
# 设置虚IP，如果没有虚IP这里设置 HAProxy的IP
VirtualIP = 192.168.20.48
# k8s 版本
K8sVersion = 1.16.6

```

* * *

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

* * *

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

* * *

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

* * *

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
    NIC: "{{ lookup('pipe', 'ls /etc/sysconfig/network-scripts/ifcfg-e*') | regex_search('[^-]+/?$') }}"
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
          line=$(netstat -lntp | grep 6443 | wc -l)
          if [ "${line}" = "0" ]; then
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
    NIC: "{{ lookup('pipe', 'ls /etc/sysconfig/network-scripts/ifcfg-e*') | regex_search('[^-]+/?$') }}"
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
          line=$(netstat -lntp | grep 6443 | wc -l)
          if [ "${line}" = "0" ]; then
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
      shell: 'docker load < {{ deploy_dir }}/images/k8s-{{ K8sVersion }}.docker'


- hosts: master[0]
  tags:
    - k8s
    - kubeadm-init
  tasks:
    - name: 删除文件
      file:
        path: '{{ deploy_dir }}/yaml/kubeadm-init.yaml'
        state: absent

    - name: 构建 kubeadm-init.yaml
      blockinfile:
        path: '{{ deploy_dir }}/yaml/kubeadm-init.yaml'
        block: |-
          apiVersion: kubeadm.k8s.io/v1beta2
          kind: ClusterConfiguration
          kubernetesVersion: v{{ K8sVersion }}
          controlPlaneEndpoint: {{ VirtualIP }}:6443

          apiServer:
            certSANs:
              - {{ VirtualIP }}

          networking:
            dnsDomain: cluster.local
            podSubnet: 10.244.0.0/16
            serviceSubnet: 10.222.0.0/16

        state: present
        create: yes
        backup: no
        unsafe_writes: yes

    - name: '将本地canal.yaml文件拷贝至 {{ inventory_hostname  }}'
      copy:
        src: './canal.yaml'
        dest: '{{ deploy_dir }}/yaml/'

```

* * *

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
        - mkdir -p $HOME/.kube
        - cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
        - chown $(id -u):$(id -g) $HOME/.kube/config

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

    - name: 将etcd证书拉到主控机
      fetch:
        src: '/etc/kubernetes/pki/etcd/{{ item }}'
        dest: '/etc/kubernetes/pki/etcd/'
        flat: 'yes'
      loop:
        - ca.crt
        - ca.key


# 加入 k8s master 集群
- hosts: master:!master[0]
  tags:
    - k8s
    - k8s-master
  vars:
    IP: "{{ hostvars[groups.master[0]].ansible_ssh_host }}"
  tasks:
    - name: 推送k8s、etcd证书到其它master主机
      copy:
        src: '/etc/kubernetes/pki'
        dest: '/etc/kubernetes/'

    - name: 获取k8s token
      delegate_to: '{{ IP }}'
      shell: kubeadm token create --print-join-command
      register: get_token

    - name: 加入到k8s master集群
      shell: '{{ get_token.stdout }} --control-plane'

    - name: 创建文件夹
      shell: '{{ item }}'
      loop:
        - mkdir -p $HOME/.kube
        - cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
        - chown $(id -u):$(id -g) $HOME/.kube/config


# 添加 k8s worker 集群
- hosts: worker
  tags:
    - k8s
    - k8s-worker
  vars:
    IP: "{{ hostvars[groups.master[0]].ansible_ssh_host }}"
  tasks:
    - name: 获取k8s token
      remote_user: root
      delegate_to: '{{ IP }}'
      shell: kubeadm token create --print-join-command
      register: get_token

    - name: 添加k8s worker集群
      shell: '{{ get_token.stdout }}'

```

* * *

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

* * *

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

* * *

###### setup.sh

```shell
#! /usr/bin/bash

set -e
cd $(cd `dirname $0`; pwd)

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


select val in ${menu[@]}
do
    echo -e "\033[36m $val: \033[0m"
    case "$val" in
        初始化各主机)
            cmds[${#cmds[@]}]=0
        ;;

        同步ntp)
            cmds[${#cmds[@]}]=1
        ;;

        部署docker)
            cmds[${#cmds[@]}]=2
        ;;

        部署k8s)
            cmds[${#cmds[@]}]=3
        ;;

        启动k8s)
            cmds[${#cmds[@]}]=4
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
start_seconds=$(date --date="$start_time" +%s)

# shell 排序去重数组
new_cmds=($(echo ${cmds[@]} | sed 's/ /\n/g'| sort | uniq))

# 批量执行
for i in ${new_cmds[@]}
do
    ${map[$i]}
done

# ========================================================================
end_time=`date +'%Y-%m-%d %H:%M:%S'`
end_seconds=$(date --date="$end_time" +%s)
echo  -e "\033[36m ==========================脚本执行时间：$[$end_seconds - $start_seconds]秒============================== \033[0m"

```

* * *

* * *

* * *
