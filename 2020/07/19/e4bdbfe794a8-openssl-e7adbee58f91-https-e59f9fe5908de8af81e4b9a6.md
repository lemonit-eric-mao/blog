---
title: '使用 Openssl 签发 https 域名证书'
date: '2020-07-19T04:31:56+00:00'
status: private
permalink: /2020/07/19/%e4%bd%bf%e7%94%a8-openssl-%e7%ad%be%e5%8f%91-https-%e5%9f%9f%e5%90%8d%e8%af%81%e4%b9%a6
author: 毛巳煜
excerpt: ''
type: post
id: 5376
category:
    - Kubernetes
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
---
###### 签发机构名

1. 国家(C)
2. 省(ST)
3. 市(L)
4. 组织机构(O)
5. 单位部门(OU)
6. 通用名(CN)
7. 邮箱地址

###### 前置条件 设定一个域名， 根据域名创建 .crt .key .p12 证书

```ruby
## 证书名
export DOMAIN_NAME=devcloud.cloud.dhc.com.cn

## 创建自签名RootCA
## 生成根证书私钥 .key
openssl genrsa -out RootCA.key 4096

## 生成自签名根证书 .crt
openssl req -new -sha256 -x509 -days 365 -key RootCA.key -out RootCA.crt -subj "/C=CN/ST=LN/L=DL/O=DHC/OU=DHC/CN=<span class="katex math inline">DOMAIN_NAME"

---

## 签发证书
##生成私钥 .key
openssl genrsa -out</span>DOMAIN_NAME.key 4096

## 申请签名 .csr
openssl req -new -sha256 -key <span class="katex math inline">DOMAIN_NAME.key -out</span>DOMAIN_NAME.csr -subj "/C=CN/ST=LN/L=DL/O=DHC/OU=DHC/CN=<span class="katex math inline">DOMAIN_NAME"

## 使用根CA证书签发生成x509格式 .crt证书
openssl x509 -req -sha256 -days 365 -CA RootCA.crt -CAkey RootCA.key -CAcreateserial -in</span>DOMAIN_NAME.csr -out <span class="katex math inline">DOMAIN_NAME.crt

## 签发 .pem证书
openssl x509 -outform PEM -in</span>DOMAIN_NAME.crt -out <span class="katex math inline">DOMAIN_NAME.pem

## 签发 .p12证书
openssl pkcs12 -export -inkey</span>DOMAIN_NAME.key -in <span class="katex math inline">DOMAIN_NAME.crt -out</span>DOMAIN_NAME.p12


```

- - - - - -

- - - - - -

- - - - - -

###### 改文件名

```ruby
[root@k8s-master tls]# mv <span class="katex math inline">DOMAIN_NAME.key tls.key
[root@k8s-master tls]# mv</span>DOMAIN_NAME.crt tls.crt

```

- - - - - -

##### 将 https 证书， 添加到k8s中

###### 添加 `TLS密文`

```ruby
# 为 secret 创建命名空间
kubectl create namespace secret-tls-ns

# 创建 secret tls
kubectl -n secret-tls-ns create secret tls tls-ingress \
  --cert=tls.crt \
  --key=tls.key

# 查看 列表
kubectl -n secret-tls-ns get secret tls-ingress

# 查看 yaml
kubectl -n secret-tls-ns get secret tls-ingress -o yaml

# 在线编辑
kubectl -n secret-tls-ns edit secret tls-ingress

# 删除
kubectl -n secret-tls-ns delete secret tls-ingress

```

- - - - - -

###### 添加 `私有 CA 签发证书`

```ruby
# 生成 私有 CA 签发证书
[root@k8s-master tls]# openssl x509 -in ca.crt -out cacerts.pem -outform PE


# 创建 secret generic
kubectl -n secret-tls-ns create secret generic tls-ca \
  --from-file=cacerts.pem


# 查看 列表
kubectl -n secret-tls-ns get secret tls-ca

# 查看 yaml
kubectl -n secret-tls-ns get secret tls-ca -o yaml

# 在线编辑
kubectl -n secret-tls-ns edit secret tls-ca

# 删除
kubectl -n secret-tls-ns delete secret tls-ca


```

- - - - - -