---
title: 'K8S 集群证书 续期'
date: '2021-05-07T09:10:59+00:00'
status: publish
permalink: /2021/05/07/k8s-%e9%9b%86%e7%be%a4%e8%af%81%e4%b9%a6-%e7%bb%ad%e6%9c%9f
author: 毛巳煜
excerpt: ''
type: post
id: 7227
category:
    - Kubernetes
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
##### 证书**`续期`**

###### 查看集群当前证书期限

**`kubeadm certs check-expiration`**

```ruby
[root@master01 ~]# kubeadm certs check-expiration
[check-expiration] Reading configuration from the cluster...
[check-expiration] FYI: You can look at this config file with 'kubectl -n kube-system get cm kubeadm-config -o yaml'

CERTIFICATE                EXPIRES                  RESIDUAL TIME   CERTIFICATE AUTHORITY   EXTERNALLY MANAGED
admin.conf                 Mar 24, 2022 03:26 UTC    10d                                    no
apiserver                  Mar 24, 2022 03:26 UTC    10d            ca                      no
apiserver-etcd-client      Mar 24, 2022 03:26 UTC    10d            etcd-ca                 no
apiserver-kubelet-client   Mar 24, 2022 03:26 UTC    10d            ca                      no
controller-manager.conf    Mar 24, 2022 03:26 UTC    10d                                    no
etcd-healthcheck-client    Mar 24, 2022 03:26 UTC    10d            etcd-ca                 no
etcd-peer                  Mar 24, 2022 03:26 UTC    10d            etcd-ca                 no
etcd-server                Mar 24, 2022 03:26 UTC    10d            etcd-ca                 no
front-proxy-client         Mar 24, 2022 03:26 UTC    10d            front-proxy-ca          no
scheduler.conf             Mar 24, 2022 03:26 UTC    10d                                    no

CERTIFICATE AUTHORITY     EXPIRES                  RESIDUAL TIME                            EXTERNALLY MANAGED
ca                        Mar 22, 2031 03:26 UTC   9y                                       no
etcd-ca                   Mar 22, 2031 03:26 UTC   9y                                       no
front-proxy-ca            Mar 22, 2031 03:26 UTC   9y                                       no
[root@master01 ~]#

```

- - - - - -

###### 为集群证书续期

**`kubeadm certs renew all`**

```ruby
[root@master01 ~]# kubeadm certs renew all
[renew] Reading configuration from the cluster...
[renew] FYI: You can look at this config file with 'kubectl -n kube-system get cm kubeadm-config -o yaml'

certificate embedded in the kubeconfig file for the admin to use and for kubeadm itself renewed
certificate for serving the Kubernetes API renewed
certificate the apiserver uses to access etcd renewed
certificate for the API server to connect to kubelet renewed
certificate embedded in the kubeconfig file for the controller manager to use renewed
certificate for liveness probes to healthcheck etcd renewed
certificate for etcd nodes to communicate with each other renewed
certificate for serving etcd renewed
certificate for the front proxy client renewed
certificate embedded in the kubeconfig file for the scheduler manager to use renewed

Done renewing certificates. You must restart the kube-apiserver, kube-controller-manager, kube-scheduler and etcd, so that they can use the new certificates.
[root@master01 ~]#

```

- - - - - -

###### 查看 PKI文件夹中的文件 **更新时间**

**你会发现`根证书并没有被更新`，所以这种做法只适合在证书没有过期的时候进行`续期`**

```ruby
[root@master01 ~]# ll /etc/kubernetes-bak/pki/
total 56
-rw-r--r--. 1 root root 1265 Aug  1 13:30 apiserver.crt
-rw-r--r--. 1 root root 1135 Aug  1 13:30 apiserver-etcd-client.crt
-rw-------. 1 root root 1675 Aug  1 13:30 apiserver-etcd-client.key
-rw-------. 1 root root 1675 Aug  1 13:30 apiserver.key
-rw-r--r--. 1 root root 1143 Aug  1 13:30 apiserver-kubelet-client.crt
-rw-------. 1 root root 1675 Aug  1 13:30 apiserver-kubelet-client.key
-rw-r--r--. 1 root root 1066 May 28  2021 ca.crt
-rw-------. 1 root root 1679 May 28  2021 ca.key
drwxr-xr-x. 2 root root  162 May 28  2021 etcd
-rw-r--r--. 1 root root 1078 May 28  2021 front-proxy-ca.crt
-rw-------. 1 root root 1675 May 28  2021 front-proxy-ca.key
-rw-r--r--. 1 root root 1103 Aug  1 13:30 front-proxy-client.crt
-rw-------. 1 root root 1679 Aug  1 13:30 front-proxy-client.key
-rw-------. 1 root root 1679 May 28  2021 sa.key
-rw-------. 1 root root  451 May 28  2021 sa.pub


```

- - - - - -

###### 再次查看集群证书期限

**`kubeadm certs check-expiration`**

```ruby
[root@master01 ~]# kubeadm certs check-expiration
[check-expiration] Reading configuration from the cluster...
[check-expiration] FYI: You can look at this config file with 'kubectl -n kube-system get cm kubeadm-config -o yaml'

CERTIFICATE                EXPIRES                  RESIDUAL TIME   CERTIFICATE AUTHORITY   EXTERNALLY MANAGED
admin.conf                 May 07, 2022 09:05 UTC   364d                                    no
apiserver                  May 07, 2022 09:05 UTC   364d            ca                      no
apiserver-etcd-client      May 07, 2022 09:05 UTC   364d            etcd-ca                 no
apiserver-kubelet-client   May 07, 2022 09:05 UTC   364d            ca                      no
controller-manager.conf    May 07, 2022 09:05 UTC   364d                                    no
etcd-healthcheck-client    May 07, 2022 09:05 UTC   364d            etcd-ca                 no
etcd-peer                  May 07, 2022 09:05 UTC   364d            etcd-ca                 no
etcd-server                May 07, 2022 09:05 UTC   364d            etcd-ca                 no
front-proxy-client         May 07, 2022 09:05 UTC   364d            front-proxy-ca          no
scheduler.conf             May 07, 2022 09:05 UTC   364d                                    no

CERTIFICATE AUTHORITY      EXPIRES                  RESIDUAL TIME                           EXTERNALLY MANAGED
ca                         Mar 22, 2031 03:26 UTC   9y                                      no
etcd-ca                    Mar 22, 2031 03:26 UTC   9y                                      no
front-proxy-ca             Mar 22, 2031 03:26 UTC   9y                                      no
[root@master01 ~]#


```

- - - - - -

- - - - - -

- - - - - -

##### 根证书也过期了怎么办？

###### 继续上面的步骤，更新所有 **`kubeconfig`** 配置文件

**`kubeadm init phase kubeconfig all --kubernetes-version 指定集群版本号`**

```ruby
kubeadm init phase kubeconfig all --kubernetes-version 1.20.4


```

- - - - - -

###### 再次查看 PKI文件夹中的文件 **更新时间**

```ruby
[root@master01 ~]# ll /etc/kubernetes/pki/
total 56
-rw-r--r--. 1 root root 1265 Aug  1 14:41 apiserver.crt
-rw-r--r--. 1 root root 1135 Aug  1 14:41 apiserver-etcd-client.crt
-rw-------. 1 root root 1675 Aug  1 14:41 apiserver-etcd-client.key
-rw-------. 1 root root 1675 Aug  1 14:41 apiserver.key
-rw-r--r--. 1 root root 1143 Aug  1 14:41 apiserver-kubelet-client.crt
-rw-------. 1 root root 1675 Aug  1 14:41 apiserver-kubelet-client.key
-rw-r--r--. 1 root root 1066 Aug  1 14:41 ca.crt
-rw-------. 1 root root 1679 Aug  1 14:41 ca.key
drwxr-xr-x. 2 root root  162 Aug  1 14:41 etcd
-rw-r--r--. 1 root root 1078 Aug  1 14:41 front-proxy-ca.crt
-rw-------. 1 root root 1675 Aug  1 14:41 front-proxy-ca.key
-rw-r--r--. 1 root root 1103 Aug  1 14:41 front-proxy-client.crt
-rw-------. 1 root root 1679 Aug  1 14:41 front-proxy-client.key
-rw-------. 1 root root 1679 Aug  1 14:41 sa.key
-rw-------. 1 root root  451 Aug  1 14:41 sa.pub
[root@master01 ~]#


```

- - - - - -

###### 重新配置 **`kubectl`**

```ruby
rm -rf /root/.kube/
mkdir -p <span class="katex math inline">HOME/.kube
cp -i /etc/kubernetes/admin.conf</span>HOME/.kube/config
chown <span class="katex math inline">(id -u):</span>(id -g) $HOME/.kube/config


```

- - - - - -

- - - - - -

- - - - - -