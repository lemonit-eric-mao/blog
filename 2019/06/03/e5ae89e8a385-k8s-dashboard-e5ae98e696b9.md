---
title: '安装 K8S Dashboard (官方)'
date: '2019-06-03T14:09:46+00:00'
status: publish
permalink: /2019/06/03/%e5%ae%89%e8%a3%85-k8s-dashboard-%e5%ae%98%e6%96%b9
author: 毛巳煜
excerpt: ''
type: post
id: 4726
category:
    - Kubernetes
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
- - - - - -

##### **[K8S dashboard 创建多用户并授予不同权限](http://www.dev-share.top/2020/04/20/k8s-dashboard-%E5%88%9B%E5%BB%BA%E5%A4%9A%E7%94%A8%E6%88%B7%E5%B9%B6%E6%8E%88%E4%BA%88%E4%B8%8D%E5%90%8C%E6%9D%83%E9%99%90/ "K8S dashboard 创建多用户并授予不同权限")**

##### **[安装 Kuboard(国产)](https://kuboard.cn/install/install-dashboard.html#%E5%AE%89%E8%A3%85 "安装 Kuboard(国产)")**

##### **[安装 K8S Dashboard 2.0](http://www.dev-share.top/2020/06/04/%E5%AE%89%E8%A3%85-k8s-dashboard-2-0/ "安装 K8S Dashboard 2.0")**

- - - - - -

##### 一、下载 kubernetes-dashboard-amd64 镜像

```ruby
docker pull registry.cn-hangzhou.aliyuncs.com/google_containers/kubernetes-dashboard-amd64:v1.10.1

docker tag registry.cn-hangzhou.aliyuncs.com/google_containers/kubernetes-dashboard-amd64:v1.10.1 k8s.gcr.io/kubernetes-dashboard-amd64:v1.10.1

docker rmi registry.cn-hangzhou.aliyuncs.com/google_containers/kubernetes-dashboard-amd64:v1.10.1

```

- - - - - -

- - - - - -

- - - - - -

##### 二、安装图形化管理界面

[k8s 的 dashboard 官方项目](https://github.com/kubernetes/dashboard "k8s 的 dashboard 官方项目")  
[dashboard 与 k8s的 兼容性](https://github.com/kubernetes/dashboard/releases "dashboard 与 k8s的 兼容性")

###### 将 github上的 yaml下载到本地安装；

```ruby
[root@k8s-master ~]# mkdir -p /home/k8s-dashboard/yamls
[root@k8s-master ~]#
[root@k8s-master ~]# wget -P /home/k8s-dashboard/yamls https://raw.githubusercontent.com/kubernetes/dashboard/v1.10.1/src/deploy/recommended/kubernetes-dashboard.yaml
[root@k8s-master ~]#
[root@k8s-master ~]# kubectl apply -f kubernetes-dashboard.yaml

```

###### 绑定 kubernetes-dashboard 角色 sa-and-crb.yaml

```ruby
cat > sa-and-crb.yaml 
```

- - - - - -

- - - - - -

- - - - - -

##### 三、配置dashboard证书

```ruby
[root@k8s-master ~]# mkdir -p /home/k8s-dashboard/tls && cd /home/k8s-dashboard/tls

```

###### 1. 创建自签名CA

**1.1 生成私钥**

```ruby
[root@k8s-master tls]# openssl genrsa -out ca.key 2048
Generating RSA private key, 2048 bit long modulus
........+++
....................+++
e is 65537 (0x10001)
[root@k8s-master tls]#
[root@k8s-master tls]# ll
总用量 4
-rw-r--r--. 1 root root 1675 1月   2 13:24 ca.key
[root@k8s-master tls]#

```

**1.2 生成自签名证书**

```ruby
[root@k8s-master tls]# openssl req -new -x509 -key ca.key -out ca.crt -days 3650 -subj "/C=CN/ST=HB/L=WH/O=DM/OU=YPT/CN=CA"
[root@k8s-master tls]#
[root@k8s-master tls]# ll
总用量 8
-rw-r--r--. 1 root root 1253 1月   2 13:24 ca.crt
-rw-r--r--. 1 root root 1675 1月   2 13:24 ca.key
[root@k8s-master tls]#

```

**1.3 查看CA内容**

```ruby
[root@k8s-master tls]# openssl x509 -in ca.crt -noout -text

```

- - - - - -

###### 2. 签发dashboard证书

**2.1 生成私钥**

```ruby
[root@k8s-master tls]# openssl genrsa -out dashboard.key 2048
Generating RSA private key, 2048 bit long modulus
....+++
...............................................................................+++
e is 65537 (0x10001)
[root@k8s-master tls]# ll
总用量 12
-rw-r--r--. 1 root root 1253 1月   2 13:24 ca.crt
-rw-r--r--. 1 root root 1675 1月   2 13:24 ca.key
-rw-r--r--. 1 root root 1679 1月   2 13:25 dashboard.key
[root@k8s-master tls]#

```

**2.2 申请签名**

```ruby
[root@k8s-master tls]# openssl req -new -sha256 -key dashboard.key -out dashboard.csr -subj "/C=CN/ST=HB/L=WH/O=DM/OU=YPT/CN=kubernetes-dashboard"
[root@k8s-master tls]# ll
-rw-r--r--. 1 root root 1253 1月   2 13:24 ca.crt
-rw-r--r--. 1 root root 1675 1月   2 13:24 ca.key
-rw-r--r--. 1 root root  989 1月   2 13:26 dashboard.csr
-rw-r--r--. 1 root root 1679 1月   2 13:25 dashboard.key
[root@k8s-master tls]#

```

**2.3 签发证书**

```ruby
[root@k8s-master tls]# openssl x509 -req -sha256 -days 3650 -in dashboard.csr -out dashboard.crt -CA ca.crt -CAkey ca.key -CAcreateserial

Signature ok
subject=/C=CN/ST=HB/L=WH/O=DM/OU=YPT/CN=172.160.180.46
Getting CA Private Key
[root@k8s-master tls]#
[root@k8s-master tls]# ll
-rw-r--r--. 1 root root 1253 1月   2 13:24 ca.crt
-rw-r--r--. 1 root root 1675 1月   2 13:24 ca.key
-rw-r--r--. 1 root root   17 1月   2 13:28 ca.srl
-rw-r--r--. 1 root root 1383 1月   2 13:28 dashboard.crt
-rw-r--r--. 1 root root  989 1月   2 13:26 dashboard.csr
-rw-r--r--. 1 root root 1679 1月   2 13:25 dashboard.key
[root@k8s-master tls]#


```

**2.4 查看证书**

```ruby
[root@k8s-master tls]# openssl x509 -in dashboard.crt -noout -text

```

- - - - - -

###### 3. 挂载证书到dashboard

**3.1 创建 secret kubernetes-dashboard-certs**

```ruby
[root@k8s-master tls]# kubectl create secret generic kubernetes-dashboard-certs --from-file="/home/k8s-dashboard/tls/dashboard.crt,/home/k8s-dashboard/tls/dashboard.key" -n kube-system

```

**3.2 查看secret内容**

```ruby
[root@k8s-master tls]# kubectl get secret kubernetes-dashboard-certs -n kube-system -o yaml

apiVersion: v1
data:
  dashboard.crt: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUR6ekNDQXJlZ0F3SUJBZ0lKQUw1Y1E4ZkVOYkpDTUEwR0NTcUdTSWIzRFFFQkN3VUFNRTh4Q3pBSkJnTlYKQkFZVEFrTk9NUXN3Q1FZRFZRUUlEQUpJUWpFTE1Ba0dBMVVFQnd3Q1YwZ3hDekFKQmdOVkJBb01Ba1JOTVF3dwpDZ1lEVlFRTERBTlpVRlF4Q3pBSkJnTlZCQU1NQWtOQk1CNFhEVEl3TURFd01qQTFNamt5TWxvWERUSTVNVEl6Ck1EQTFNamt5TWxvd1d6RUxNQWtHQTFVRUJoTUNRMDR4Q3pBSkJnTlZCQWdNQWtoQ01Rc3dDUVlEVlFRSERBSlgKU0RFTE1Ba0dBMVVFQ2d3Q1JFMHhEREFLQmdOVkJBc01BMWxRVkRFWE1CVUdBMVVFQXd3T01Ua3lMakUyT0M0eApPREF1TkRZd2dnRWlNQTBHQ1NxR1NJYjNEUUVCQVFVQUE0SUJEd0F3Z2dFS0FvSUJBUUR4MStzdFlPV3JJZVpYCjg2ZnBueFIvM2theVVUNVlFY1NQcnRuM0RwSnV3a3pRbTc2c1NsZjRBaG41c3h6cGJBSVFCQ2FQWGdxd2VDQUYKelkzekRoRWVQVXhyWEd1dFpaN0lwcUdKM0M1K2ZmdkpIdnJPa0VHaTI2Zkw2d1NpYzZiZ0FOb1lqWmVxd1h1Uwo4dzhXWWVBZ2F4TFN6RGpPY1NqSXdOTTZrVEc0eHAzcS9SR21veUx2SEt3LzFGMzNNYU12NkRRRmZ3YS9Zd2xICndyVlFuZXFzMW9JOFlPTGg0QnJlZEtIZEFKQXJSU1g2VG9kRkg3NG5YSXVzclFncXZOdUVIejdlTzMzemt1bTUKMCs4dkFhN1ozVmNTV1hhbVZjZ0YyTURDUy8xcmIrZ1UzU1F2RlVPN0JCdUs1MnlhZFN5SlIzc0d1WTJLdjB5WgovV0VMSzdvVEFnTUJBQUdqZ2FFd2daNHdDd1lEVlIwUEJBUURBZ2VBTUIwR0ExVWRKUVFXTUJRR0NDc0dBUVVGCkJ3TUNCZ2dyQmdFRkJRY0RBVEFkQmdOVkhRNEVGZ1FVb05mcVlBQmU2RWJ0aXovd01XYUFtemw2SElJd0h3WUQKVlIwakJCZ3dGb0FVK3d2TFhFYk1vME4zZHp5NEtXZjBhckViNXlZd01BWURWUjBSQkNrd0o0Y0V3S2kwTG9jRQpmd0FBQVlJT01Ua3lMakUyT0M0eE9EQXVORGFDQ1d4dlkyRnNhRzl6ZERBTkJna3Foa2lHOXcwQkFRc0ZBQU9DCkFRRUFuRVZYN2FRQ3AwT2ZwYURIWmNyYWI3QmdzZmQ3OW9MKzlZaW5uL1dQNlp0K0pzaHAzdDF1cnVEdmxZdE0KVXNpRUFJckFndzFua3NDSTNIZWp3ZE95K3NEQ3A1N2p6WWcwckpvWjRSV0Q4S2JxUkhvWHRMSHVBQXlSbVoxbQowWlBKRnZCdk9ReHUwckd2SU5pYjlVWFFmZWU2NUp1cXVaVktRUE1kOUY2MjZhUEt4RmkxekJYU0xpMG5UeFBRCmZTemE4U1k1a2ZrS21QTHQvSEgxVWZaa203cEh1bUpjdUhOS29lcU1VY3ExUlBIWmlLUmZHUElXV1hpTFpQT1IKMzd2ZXlPYUpEWFVXbWZHLzBoQUZjQk9vdkdYeCt6dzFnWGhGSEFJZXZocXEzaGplWTk3SFRKcVIybGNUV3VpbwptbzRZMGtPekJRSm5jVm1zOWwzZEJwU3cvdz09Ci0tLS0tRU5EIENFUlRJRklDQVRFLS0tLS0K
  dashboard.key: LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVktLS0tLQpNSUlFcFFJQkFBS0NBUUVBOGRmckxXRGxxeUhtVi9PbjZaOFVmOTVHc2xFK1dCSEVqNjdaOXc2U2JzSk0wSnUrCnJFcFgrQUlaK2JNYzZXd0NFQVFtajE0S3NIZ2dCYzJOOHc0UkhqMU1hMXhycldXZXlLYWhpZHd1Zm4zN3lSNzYKenBCQm90dW55K3NFb25PbTRBRGFHSTJYcXNGN2t2TVBGbUhnSUdzUzBzdzR6bkVveU1EVE9wRXh1TWFkNnYwUgpwcU1pN3h5c1A5UmQ5ekdqTCtnMEJYOEd2Mk1KUjhLMVVKM3FyTmFDUEdEaTRlQWEzblNoM1FDUUswVWwrazZIClJSKytKMXlMckswSUtyemJoQjgrM2p0OTg1THB1ZFB2THdHdTJkMVhFbGwycGxYSUJkakF3a3Y5YTIvb0ZOMGsKTHhWRHV3UWJpdWRzbW5Vc2lVZDdCcm1OaXI5TW1mMWhDeXU2RXdJREFRQUJBb0lCQUVoV3NIYlRXLzlUVllZTApVTGQxcVBrU2NJMFg5aEQ3eDVLKzExMnAweTBrR3p2dXloclk1ZlUrRTZ6MzRYY0VvcDFOMElianQwalB0YXhtCnJzWDcrQ3pXWXd4ZUNhdEZFVGl0ZHZZNGtRT3ZCV2hFUnZzUWRVR1VlRjFyZitoanRZK2RVWjgwZ3lCRlhZUTQKQmRSSkZIUTk4dFJ3MTdFUWNnV1NmOXd0My9TSGg0ZUh2YlRGUjBGY0d6OWlTM0lsREh2cTlINERzRW4xdnBJWQpaWEwvaUtBYmFuUDBvYm9rRVNxdlNHT3N3ZW9XOEc2OHFZMFdaRmFmRHhRSmxWNUdFUUdjNVplVzJ0UkFQUUY1Ck1hV3pPQWt3Sm1CZXY0RG92L2lSRDVNSlp5VUI3aVFDd2YxOHhDK1IxYnorWHQwdTRTMmVobmtuZWZ0Mm84OS8KTUxZTk1Ga0NnWUVBL05BSXEvMWxVVjBLMlJFWXVXblNjeU13OVg4WGF2b2U3VTJoZDY3QUJRQ05FTnBMcFBPWApCS3lWK2R4QVlHKy9NcmhCeHpTalJQeGVZZllXU2VxZDhzRElPSEZ0SDQyVHRqYVFZeXJhMTc3K0NIdDdYVmU2CmhMTUtDbkU0WEJDcU05WUVVTi9pbUVFRUxlclpNL0MrbThDZVFwRkRxdk5JYWZ1ZHMwMlF4ajBDZ1lFQTlPUjcKS2t6Y1dCL2dBbFZBS0M3NUtTcjdPYWVCNnpvOHNxRmhPVTMySTlid0VrRkFRQVh6bFh4L1VxeXNhNDhPK1U4RQpNVlNRa043SmZHY3F3Nkg3SERoNEtxOGtJdUxhOGdtZFU5bVJQTG4vSEtUZzVTcUI2cVd1VDNZQ0t2RHowSFJHCkNpc0FQVWRIQk1TMkhOT1ZtVytDY2sxbE81cW40VDdpZWlkTzFvOENnWUVBemZobnVFaEFqYU55UFJ0eXUweisKQ3BRM1JTd0FWa1hsZ0l6bzZtdFRRa0FLcmhwTDJ0NGl3Y29pZm1qMWdoeEk5L2VxajdQUStWbHJSQUNNZERoVAo2djBwb3VLMmR5aVBtYnFtdEVTcisyNDk1WWRGSU8xaXBzNS9kYlo4cG5WbFZjb2R4ZzVCdkszcnk4VTBwTjZWClRLd0h4RkE1ZzBPbVVjS1AzdzlvemprQ2dZRUE2SG0xeWxRb29LZXh1Y1ZBSUdWbk5vT005aEJrTHUrY0MxOVQKc2xpbUh5Tzl4emFXVGJEWXFjSUVCSEhUUkZBTVFQT1g0VlNMNEZyK0h0QzVNZm9sTFljVjNEOWpLSkwra2VJNgpyZ3pONlQ0UVJocm5PK1Y4YTBwWkRTblRxUHdRR0lVb3NDSmVHYzMrUnpLT1J4TTg0dW1PaGYrZTZGUktwbk5SCi8vQXMwVlVDZ1lFQTdKYzFid3RZd3dCS3dwK0xjZkttV3puWkM0bTkyT2pIempuVnA2MkVxd3pYbkF5SzFDR2gKKzdsaStyRVgrVS82eVorZjFrUHpFODBXZ0o2QTNqWG95dWNaejNYdGpYRVNCWUdHTGorZ1JlTGF1VFd4RkMzMwoxRVVJa2FGS1U3NUs0YWdSTFRXOTJ6REJPV1VWaWM5aHdnT0xTNFBuTFF4WUZwQlFEUGZPTk1zPQotLS0tLUVORCBSU0EgUFJJVkFURSBLRVktLS0tLQo=
kind: Secret
metadata:
  creationTimestamp: "2020-01-02T05:37:32Z"
  name: kubernetes-dashboard-certs
  namespace: kube-system
  resourceVersion: "191976"
  selfLink: /api/v1/namespaces/kube-system/secrets/kubernetes-dashboard-certs
  uid: f8dbfa0e-2d21-11ea-ae6d-005056970e35
type: Opaque
[root@k8s-master tls]#


```

**3.3 启动dashboard**

```ruby
# 启动
[root@k8s-master tls]# kubectl apply -f /home/k8s-dashboard/yamls/sa-and-crb.yaml -f /home/k8s-dashboard/yamls/kubernetes-dashboard.yaml
[root@k8s-master tls]#

# 查看 service
[root@k8s-master tls]# kubectl get svc,pod --all-namespaces | grep kubernetes-dashboard

kube-system   service/kubernetes-dashboard   ClusterIP   10.97.156.72   <none>        443/TCP         2m5s
kube-system   pod/kubernetes-dashboard-57df4db6b-kzlhd   1/1     Running   0          2m5s
[root@k8s-master tls]#
</none>
```

**3.4 获取 token**

```ruby
[root@k8s-master yamls]# kubectl describe secret kubernetes-dashboard -n kube-system
Name:         kubernetes-dashboard-certs
Namespace:    kube-system
Labels:       k8s-app=kubernetes-dashboard
Annotations:
Type:         Opaque

Data
====
dashboard.crt:  1383 bytes
dashboard.key:  1679 bytes

Name:         kubernetes-dashboard-key-holder
Namespace:    kube-system
Labels:       <none>
Annotations:  <none>

Type:  Opaque

Data
====
pub:   459 bytes
priv:  1679 bytes

Name:         kubernetes-dashboard-token-dlcg7
Namespace:    kube-system
Labels:       <none>
Annotations:  kubernetes.io/service-account.name: kubernetes-dashboard
              kubernetes.io/service-account.uid: eabfc67c-2d35-11ea-961b-005056970e35

Type:  kubernetes.io/service-account-token

Data
====
namespace:  11 bytes
token:      eyJhbGciOiJSUzI1NiIsImtpZCI6IiJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJrdWJlcm5ldGVzLWRhc2hib2FyZC10b2tlbi1kbGNnNyIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50Lm5hbWUiOiJrdWJlcm5ldGVzLWRhc2hib2FyZCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6ImVhYmZjNjdjLTJkMzUtMTFlYS05NjFiLTAwNTA1Njk3MGUzNSIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDprdWJlLXN5c3RlbTprdWJlcm5ldGVzLWRhc2hib2FyZCJ9.QVItAq_ocOCSZjTh5TRNKUANfmyqxwVIuRlZEO7ZcRpXiCLqu5c0HnxCpcixBwg4jkdUOD0q9sPgvi5K6DnOvxltUJITf39pKn5-WEv0uZYM4YrOLtZw7YGtZwQhvjUX_NJrnz3vx0jUmbPUejU2Q9FeC1yUMBGYP2RZPeKcyxh69Pjn-4iPgK3GlwRSXOK9LcIkXu0gpm-QbNLWCMNrqLAbpJ9iBPizZjuxyL-RH3-PS09EvbLU1rziDNShOo4_wuRIMR4V9PaP4xj5mNGjFuGbo1DwPqP-bmc8V1sSBvFAviOLt_A1nUzoAZX_i-5nXA8kukoFXyfDWuC7cqDqjQ
ca.crt:     1025 bytes

[root@k8s-master yamls]#

</none></none></none>
```

**3.5 生成 `kubecfg.p12` 证书，给浏览器用**

```ruby
[root@k8s-master tls]# grep 'client-certificate-data' ~/.kube/config | head -n 1 | awk '{print <span class="katex math inline">2}' | base64 -d > kubecfg.crt
[root@k8s-master tls]# grep 'client-key-data' ~/.kube/config | head -n 1 | awk '{print</span>2}' | base64 -d > kubecfg.key
[root@k8s-master tls]# openssl pkcs12 -export -clcerts -inkey kubecfg.key -in kubecfg.crt -out kubecfg.p12 -name "kubernetes-client"

```

**3.6 web访问**：https://172.160.180.46:6443/api/v1/namespaces/kube-system/services/https:kubernetes-dashboard:/proxy/

- - - - - -

- - - - - -

- - - - - -

##### 四、彻底删除 dashboard

```ruby
# 查看要删除的 secret
[root@k8s-master tls]# kubectl get secret -n kube-system | grep dashboard
kubernetes-dashboard-certs                       Opaque                                2      12m
kubernetes-dashboard-key-holder                  Opaque                                2      12m
kubernetes-dashboard-token-r768d                 kubernetes.io/service-account-token   3      12m
[root@k8s-master tls]#
[root@k8s-master tls]#
[root@k8s-master tls]# kubectl delete -f /home/k8s-dashboard/yamls/sa-and-crb.yaml -f /home/k8s-dashboard/yamls/kubernetes-dashboard.yaml
[root@k8s-master tls]#
[root@k8s-master tls]#
[root@k8s-master tls]# kubectl get secret -n kube-system | grep dashboard | xargs kubectl delete -n kube-system secret

```

- - - - - -

- - - - - -

- - - - - -

##### 编写安装脚本(复制直接用) dashboard-install.sh

```shell
cat > dashboard-install.sh  /home/k8s-dashboard/yamls/kubernetes-dashboard.yaml  /home/k8s-dashboard/yamls/sa-and-crb.yaml 
```

- - - - - -

##### 编写卸载脚本 dashboard-uninstall.sh

```shell
cat > dashboard-uninstall.sh 
```

- - - - - -

- - - - - -

- - - - - -

##### 扩展知识点 什么是 ServiceAccount

**k8s 有两种账户:**

1. 给机器用的 **ServiceAccount**
2. 给人用的 **UserAccount**

- - - - - -

###### `上面部署的 dashboard 是通过配置 .yaml 文件的方式进行的账户角色绑定；以下使用手动创建账户方式，来说明 ServiceAccount 作用`

###### 1. 手动创建 ServiceAccount

```ruby
# 创建一个名为 sa-admin的 ServiceAccount 账户，并将它加入到 kube-system命名空间下
[root@k8s-master ~]# kubectl create serviceaccount sa-admin -n kube-system
serviceaccount/def-ns-admin created
[root@k8s-master ~]#
[root@k8s-master ~]# kubectl get sa -A
# 命名空间         ServiceAccount
NAMESPACE         NAME                                 SECRETS   AGE
default           default                              1         5d5h
kube-node-lease   default                              1         5d5h
kube-public       default                              1         5d5h
kube-system       sa-admin                             1         21s
kube-system       attachdetach-controller              1         5d5h
......
[root@k8s-master ~]#

```

###### 2. 删除 ServiceAccount账户

```ruby
[root@k8s-master ~]# kubectl serviceaccount sa sa-admin -n kube-system
rolebinding.rbac.authorization.k8s.io "sa-admin" deleted

```

###### 3. 查看 k8s 默认角色

```ruby
[root@k8s-master ~]# kubectl get clusterrole -A | grep cluster-admin
cluster-admin                                                          5d5h
[root@k8s-master ~]#

```

###### 4. 把ServiceAccount绑定在cluster集群角色上, 让它享有集群管理员的权限

**创建一个名为 sa-admin-role的集群角色绑定，并将kube-system命名空间下的sa-admin （ServiceAccount账户），赋予clusterrole的cluster-admin权限**

```ruby
[root@k8s-master ~]# kubectl create clusterrolebinding sa-admin-role --clusterrole=cluster-admin --serviceaccount=kube-system:sa-admin
clusterrolebinding.rbac.authorization.k8s.io/sa-admin-role created
[root@k8s-master ~]#

```

###### 5. 查看新建的角色

```ruby
[root@k8s-master ~]# kubectl get clusterrolebinding | grep sa-admin-role
sa-admin-role                                          31s
[root@k8s-master ~]#
[root@k8s-master ~]# kubectl describe clusterrolebinding sa-admin-role
Name:         sa-admin-role
Labels:       <none>
Annotations:  <none>
Role:
  Kind:  ClusterRole
  Name:  cluster-admin
Subjects:
  Kind            Name      Namespace
  ----            ----      ---------
  ServiceAccount  sa-admin  kube-system
[root@k8s-master ~]#
</none></none>
```

###### 6. 删除role

```ruby
[root@k8s-master ~]# kubectl delete clusterrolebinding sa-admin-role
clusterrolebinding.rbac.authorization.k8s.io "sa-admin-role" deleted

```

###### 7. 查看sa-admin的token

```ruby
**使用token登录, 其实就是告诉k8s使用了哪个 ServiceAccount账户进行操作 dashboard**
[root@k8s-master ~]# kubectl describe secret sa-admin -n kube-system
Name:         sa-admin-token-4bktz
Namespace:    kube-system
Labels:       <none>
Annotations:  kubernetes.io/service-account.name: sa-admin
              kubernetes.io/service-account.uid: ee40378d-8c24-11e9-af9f-00163e02a4bf

Type:  kubernetes.io/service-account-token

Data
====
ca.crt:     1025 bytes
namespace:  11 bytes
token:      eyJhbGciOiJSUzI1NiIsImtpZCI6IiJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJzYS1hZG1pbi10b2tlbi00Ymt0eiIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50Lm5hbWUiOiJzYS1hZG1pbiIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6ImVlNDAzNzhkLThjMjQtMTFlOS1hZjlmLTAwMTYzZTAyYTRiZiIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDprdWJlLXN5c3RlbTpzYS1hZG1pbiJ9.ZnlKKgAEyeZBvYj6AZV1plXZz0RjdMz6-Vl607_M_IaR1SvNJPV307tT6g69uViQBqRi1yxvUWEvpwqUQazDpNV2IPxmXd1qMm6L6sWwrvsMcnK3jPjLIlWV3ospnh9x14tJqnBVH1Z7-do7IyUvsj7XGk707Q-xXKmXGW0s9gARKLP8a61gxdDNnuCboUJt3Apxrq6rgcmY5kq4HBcJ-W7cr0ldtz6adTCqn1Mlfug86jZZCbT0UhqsSk5mPzHMtf44X29FjPV_FkGDywtU8ZNPQiWDJI7xAti9WGBOEzPc1Lfw0WnQLLsPpa5npKotKlApCwbiuBo-XLAU_gNlDQ

[root@k8s-master ~]#
</none>
```

- - - - - -

- - - - - -

- - - - - -