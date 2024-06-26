---
title: "ElasticSearch 安装插件"
date: "2019-10-24"
categories: 
  - "elasticsearch"
---

##### 离线安装分词器

###### [官网地址](https://github.com/KennFalcon/elasticsearch-analysis-hanlp "官网地址") 这个是HanLP为了支持ES，开发的插件

###### [官方下载地址](https://github.com/KennFalcon/elasticsearch-analysis-hanlp/releases "官方下载地址")

###### [官方收录](https://github.com/hankcs/HanLP/wiki/%E8%A1%8D%E7%94%9F%E9%A1%B9%E7%9B%AE#elasticsearch-analysis-hanlpkennfalcon "官方收录")

###### 1\. 下载分词器

```ruby
[elasticsearch@test1 download]$ pwd
/home/elasticsearch/download
[elasticsearch@test1 download]$ wget https://github.com/KennFalcon/elasticsearch-analysis-hanlp/releases/download/v7.3.2/elasticsearch-analysis-hanlp-7.3.2.zip
```

###### 2.安装到ES

###### 2.1 **`单机`**安装到ES

```ruby
[elasticsearch@test1 elasticsearch-7.3.2]$ /home/elasticsearch/deploy/elasticsearch-7.3.2/bin/elasticsearch-plugin install file:///home/elasticsearch/download/elasticsearch-analysis-hanlp-7.3.2.zip
-> Downloading file:///home/elasticsearch/download/elasticsearch-analysis-hanlp-7.3.2.zip
[=================================================] 100%
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@     WARNING: plugin requires additional permissions     @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
* java.io.FilePermission <<ALL FILES>> read,write,delete
* java.lang.RuntimePermission getClassLoader
* java.lang.RuntimePermission setContextClassLoader
* java.net.SocketPermission * connect,resolve
* java.util.PropertyPermission * read,write
See http://docs.oracle.com/javase/8/docs/technotes/guides/security/permissions.html
for descriptions of what these permissions allow and the associated risks.

Continue with installation? [y/N]y
-> Installed analysis-hanlp
[elasticsearch@test1 elasticsearch-7.3.2]$
```

###### 2.1.1 修改配置文件

1. 修改配置文件 `/home/elasticsearch/deploy/elasticsearch-7.3.2/config/jvm.options` 在文件末尾追加如下文件路径 `-Djava.security.policy=/home/elasticsearch/deploy/elasticsearch-7.3.2/plugins/analysis-hanlp/plugin-security.policy`
2. 修改配置文件 `/home/elasticsearch/deploy/elasticsearch-7.3.2/config/analysis-hanlp/hanlp.properties` 将root=的值改为绝对路径 `root=/home/elasticsearch/deploy/elasticsearch-7.3.2/plugins/analysis-hanlp/`

###### 2.2 **`集群安装`**使用ansible-playbook

```ruby
[elasticsearch@test1 deploy]$ cat > setup-plugins.yml << eric
# 使用方法 ansible-playbook -i hosts.ini setup-plugins.yml
---
- hosts: servers
  tasks:
    - name: 创建deploy目录
      shell: 'mkdir -p /home/elasticsearch/download/'

    - name: '上传文件'
      # 将本地文件复制到远程服务器
      copy:
        src: '{{ item.src }}'
        dest: '{{ item.dest }}'
      with_items:
        - { src: '/home/elasticsearch/download/elasticsearch-analysis-hanlp-{{ version }}.zip', dest: '/home/elasticsearch/download/elasticsearch-analysis-hanlp-{{ version }}.zip' }

    - name: 安装HanLP插件
      shell: 'setsid { deploy_dir }}/elasticsearch-{{ version }}/bin/elasticsearch-plugin install file:///home/elasticsearch/download/elasticsearch-analysis-hanlp-{{ version }}.zip &'

    - name: 修改配置文件 jvm.options
      lineinfile:
        # /home/elasticsearch/deploy/elasticsearch-7.3.2/config/jvm.options
        dest: '{{ deploy_dir }}/elasticsearch-{{ version }}/config/jvm.options'
        line: '{{ item.value }}'
        regexp: '^{{ item.value }}.*'
        state: present
      # 定义集合，并循环执行所在的模块
      with_items:
          # 在文件末尾追加如下文件路径 -Djava.security.policy=/home/elasticsearch/deploy/elasticsearch-7.3.2/plugins/analysis-hanlp/plugin-security.policy
        - { value: '-Djava.security.policy={{ deploy_dir }}/elasticsearch-{{ version }}/plugins/analysis-hanlp/plugin-security.policy' }

    - name: 修改配置文件 hanlp.properties
      lineinfile:
        # /home/elasticsearch/deploy/elasticsearch-7.3.2/config/analysis-hanlp/hanlp.properties
        dest: '{{ deploy_dir }}/elasticsearch-{{ version }}/config/analysis-hanlp/hanlp.properties'
        line: '{{ item.key }}={{ item.value }}'
        regexp: '^{{ item.key }}.*'
        state: present
      # 定义集合，并循环执行所在的模块
      with_items:
          # 改为绝对路径 root=/home/elasticsearch/deploy/elasticsearch-7.3.2/plugins/analysis-hanlp/
        - { key: 'root', value: '{{ deploy_dir }}/elasticsearch-{{ version }}/plugins/analysis-hanlp/' }
eric

[elasticsearch@test1 deploy]$
```

###### 3\. 重启ES

###### 4\. 查看安装是否成功

```ruby
curl -X GET "http://172.160.180.47:9200/_analyze" -H "Content-Type: application/json" -d '
{
    "text": "我们大家的中华人民共和国"
}'

# 默认不使用分词器的查询结果
{
  "tokens": [
    {
      "token": "我",
      "start_offset": 0,
      "end_offset": 1,
      "type": "<IDEOGRAPHIC>",
      "position": 0
    },
    {
      "token": "们",
      "start_offset": 1,
      "end_offset": 2,
      "type": "<IDEOGRAPHIC>",
      "position": 1
    },
    {
      "token": "大",
      "start_offset": 2,
      "end_offset": 3,
      "type": "<IDEOGRAPHIC>",
      "position": 2
    },
    {
      "token": "家",
      "start_offset": 3,
      "end_offset": 4,
      "type": "<IDEOGRAPHIC>",
      "position": 3
    },
    {
      "token": "的",
      "start_offset": 4,
      "end_offset": 5,
      "type": "<IDEOGRAPHIC>",
      "position": 4
    },
    {
      "token": "中",
      "start_offset": 5,
      "end_offset": 6,
      "type": "<IDEOGRAPHIC>",
      "position": 5
    },
    {
      "token": "华",
      "start_offset": 6,
      "end_offset": 7,
      "type": "<IDEOGRAPHIC>",
      "position": 6
    },
    {
      "token": "人",
      "start_offset": 7,
      "end_offset": 8,
      "type": "<IDEOGRAPHIC>",
      "position": 7
    },
    {
      "token": "民",
      "start_offset": 8,
      "end_offset": 9,
      "type": "<IDEOGRAPHIC>",
      "position": 8
    },
    {
      "token": "共",
      "start_offset": 9,
      "end_offset": 10,
      "type": "<IDEOGRAPHIC>",
      "position": 9
    },
    {
      "token": "和",
      "start_offset": 10,
      "end_offset": 11,
      "type": "<IDEOGRAPHIC>",
      "position": 10
    },
    {
      "token": "国",
      "start_offset": 11,
      "end_offset": 12,
      "type": "<IDEOGRAPHIC>",
      "position": 11
    }
  ]
}
```

```ruby
curl -X GET "http://172.160.180.47:9200/_analyze" -H "Content-Type: application/json" -d '
{
    "text": "我们大家的中华人民共和国",
    "analyzer": "hanlp"
}'
# 使用分词器后的查询结果
{
  "tokens": [
    {
      "token": "我们",
      "start_offset": 0,
      "end_offset": 2,
      "type": "rr",
      "position": 0
    },
    {
      "token": "大家",
      "start_offset": 2,
      "end_offset": 4,
      "type": "rr",
      "position": 1
    },
    {
      "token": "的",
      "start_offset": 4,
      "end_offset": 5,
      "type": "ude1",
      "position": 2
    },
    {
      "token": "中华人民共和国",
      "start_offset": 5,
      "end_offset": 12,
      "type": "ns",
      "position": 3
    }
  ]
}


```
