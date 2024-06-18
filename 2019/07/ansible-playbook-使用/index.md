---
title: "Ansible-playbook 使用"
date: "2019-07-22"
categories: 
  - "ansible"
---

##### 1.配置远程服务器

```ruby
[gitlab-runner@k8s-master ~]$ sudo cat > /etc/ansible/hosts << eric
[webservers]
# 两种配置方式，第一种 密码需要手动输入
192.168.192.10
# 两种配置方式，第二种 先配置好用户名、密码
# 192.168.192.10 ansible_ssh_user="root" ansible_ssh_pass="redhat"
eric
[gitlab-runner@k8s-master ~]$
```

##### 2.1配置执行文件(做为 python 使用的模板)

```yaml
[gitlab-runner@k8s-master ~]$ pwd
/home/gitlab-runner
[gitlab-runner@k8s-master ~]$ cat > ansible-deploy-prod.yaml << eric
# 使用 ansible-playbook 推送生产服使用的配置文件，并执行自动部署
# 使用方法 ansible-playbook ansible-deploy-prod.yaml --ask-pass
---
- hosts: webservers
  remote_user: root

  vars:
    # 自定义变量，接收参数，拼接路径
    input: '/home/gitlab-runner/paas-devops-script/dist/{{group}}/{{tag}}/{{project_name}}/'
    output: '/home/deploy/prod/{{group}}/{{tag}}/{{project_name}}/'

  tasks:
    - name: '创建工作目录'
      # 按照拼接好的路径创建目录
      shell: mkdir -p '{{output}}'
    - name: '复制文件'
      # 将本地文件复制到远程生产服
      copy:
        src: '{{ item.src }}'
        dest: '{{ item.dest }}'
      with_items:
        - { src: '{{input}}{{project_name}}-deploy.yaml', dest: '{{output}}{{project_name}}-deploy.yaml' }
        - { src: '{{input}}{{project_name}}-hpa.yaml', dest: '{{output}}{{project_name}}-hpa.yaml' }
        - { src: '{{input}}{{project_name}}-service.yaml', dest: '{{output}}{{project_name}}-service.yaml' }
    # 以下命令是自动部署k8s语句，文档只展示语句的各种使用场景
    - name: '删除{{project_name}}容器'
      shell: 'kubectl delete -f {{output}}{{project_name}}-deploy.yaml'
      # 即使删除语句执行出错，也要继续执行(忽略异常)
      ignore_errors: yes
    - name: '部署{{project_name}}容器'
      shell: 'kubectl apply -f {{output}}'
eric
[gitlab-runner@k8s-master ~]$
```

##### 2.2生成后的配置执行文件

```yaml
# 使用 ansible-playbook 推送生产服使用的配置文件，并执行自动部署
# 使用方法 ansible-playbook ansible-deploy-prod.yaml --ask-pass
---
- hosts: webservers
  remote_user: root

  vars:
    # 自定义变量，接收参数，拼接路径
    input: '/home/gitlab-runner/paas-devops-script/dist/hrbm/tag-20190722/006-webapp/prod/'
    output: '/home/deploy/prod/hrbm/tag-20190722/006-webapp/'

  tasks:
    - name: '创建工作目录'
      # 按照拼接好的路径创建目录
      shell: mkdir -p '{{output}}'
    - name: '复制文件'
      # 将本地文件复制到远程生产服
      copy:
        src: '{{ item.src }}'
        dest: '{{ item.dest }}'
      with_items:
        - { src: '{{input}}006-webapp-deploy.yaml', dest: '{{output}}006-webapp-deploy.yaml' }
        - { src: '{{input}}006-webapp-hpa.yaml', dest: '{{output}}006-webapp-hpa.yaml' }
        - { src: '{{input}}006-webapp-service.yaml', dest: '{{output}}006-webapp-service.yaml' }
    - name: '删除201-hrbm-hrbmweb容器'
      shell: 'kubectl delete -f {{output}}006-webapp-deploy.yaml'
      # 即使删除语句执行出错，也要继续执行
      ignore_errors: yes
    - name: '部署006-webapp容器'
      shell: 'kubectl apply -f {{output}}006-webapp-deploy.yaml'
```

##### 3.手动输入密码，更安全

```ruby
[gitlab-runner@k8s-master ~]$ pwd
/home/gitlab-runner
[gitlab-runner@k8s-master ~]$ ll
-rw-rw-r-- 1 gitlab-runner gitlab-runner  114 7月  22 16:41 ansible-deploy-prod.yaml
[gitlab-runner@k8s-master ~]$
[gitlab-runner@k8s-master ~]$  ansible-playbook ansible-deploy-prod.yaml --extra-vars="group=hrbm tag=tag-20190722 project_name=006-webapp" --ask-pass
SSH password:

PLAY [webservers] *********************************************************************************************************************************************************************************

TASK [Gathering Facts] ****************************************************************************************************************************************************************************
ok: [192.168.192.10]

TASK [创建工作目录] *************************************************************************************************************************************************************************************
 [WARNING]: Consider using the file module with state=directory rather than running 'mkdir'.  If you need to use command because file is insufficient you can add 'warn: false' to this command
task or set 'command_warnings=False' in ansible.cfg to get rid of this message.

changed: [192.168.192.10]

TASK [复制文件] ***************************************************************************************************************************************************************************************
changed: [192.168.192.10] => (item={u'dest': u'/home/deploy/prod/hrbm/tag-20190722/006-webapp/006-webapp-deploy.yaml', u'src': u'/home/gitlab-runner/paas-devops-script/dist/hrbm/tag-20190722/006-webapp/006-webapp-deploy.yaml'})
changed: [192.168.192.10] => (item={u'dest': u'/home/deploy/prod/hrbm/tag-20190722/006-webapp/006-webapp-hpa.yaml', u'src': u'/home/gitlab-runner/paas-devops-script/dist/hrbm/tag-20190722/006-webapp/006-webapp-hpa.yaml'})
changed: [192.168.192.10] => (item={u'dest': u'/home/deploy/prod/hrbm/tag-20190722/006-webapp/006-webapp-service.yaml', u'src': u'/home/gitlab-runner/paas-devops-script/dist/hrbm/tag-20190722/006-webapp/006-webapp-service.yaml'})

TASK [删除容器] ***************************************************************************************************************************************************************************************
changed: [192.168.192.10]

TASK [部署容器] ***************************************************************************************************************************************************************************************
changed: [192.168.192.10]

PLAY RECAP ****************************************************************************************************************************************************************************************
192.168.192.10             : ok=3    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[gitlab-runner@k8s-master ~]$
```

* * *

* * *

* * *

##### `常见问题`

```ruby
mkdir: cannot create directory '/root/.ansible': No space left on device
# 原因
ansible-playbook 初始化时会 先在远程主机创建 '/root/.ansible'文件夹，此问题是因为远程主机上硬盘空间满了。
```

* * *

* * *

* * *
