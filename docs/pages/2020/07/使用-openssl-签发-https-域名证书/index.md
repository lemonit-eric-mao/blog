---
title: "使用 Openssl 签发 https 域名证书"
date: "2020-07-19"
categories: 
  - "k8s"
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
openssl req -new -sha256 -x509 -days 365 -key RootCA.key -out RootCA.crt -subj "/C=CN/ST=LN/L=DL/O=DHC/OU=DHC/CN=$DOMAIN_NAME"

---

## 签发证书
##生成私钥 .key
openssl genrsa -out $DOMAIN_NAME.key 4096

## 申请签名 .csr
openssl req -new -sha256 -key $DOMAIN_NAME.key -out $DOMAIN_NAME.csr -subj "/C=CN/ST=LN/L=DL/O=DHC/OU=DHC/CN=$DOMAIN_NAME"

## 使用根CA证书签发生成x509格式 .crt证书
openssl x509 -req -sha256 -days 365 -CA RootCA.crt -CAkey RootCA.key -CAcreateserial -in $DOMAIN_NAME.csr -out $DOMAIN_NAME.crt

## 签发 .pem证书
openssl x509 -outform PEM -in $DOMAIN_NAME.crt -out $DOMAIN_NAME.pem

## 签发 .p12证书
openssl pkcs12 -export -inkey $DOMAIN_NAME.key -in $DOMAIN_NAME.crt -out $DOMAIN_NAME.p12

```

* * *

* * *

* * *

###### 改文件名

```ruby
[root@k8s-master tls]# mv $DOMAIN_NAME.key tls.key
[root@k8s-master tls]# mv $DOMAIN_NAME.crt tls.crt
```

* * *

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

* * *

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

* * *
