---
title: "K8S 多集群切换"
date: "2020-09-29"
categories: 
  - "k8s"
---

###### 前置条件**对k8s`初始化部署`有要求**

```yaml
# BEGIN ANSIBLE MANAGED BLOCK
apiVersion: kubeadm.k8s.io/v1beta2
kind: ClusterConfiguration
kubernetesVersion: v1.20.4
imageRepository: k8s.gcr.io
controlPlaneEndpoint: 192.168.103.231:6443         # 在k8s所在的内网IP，集群之前会使用这个IP地址进行通信

# 只在部署高可用时配置 apiServer
apiServer:
  # 这是生成~/.kube/config证书的配置；
  # 目的是告诉生成的证书，都允许使用哪些IP地址访问ApiServer
  # 这里只是针对证书的生成与请求地址的认证，这与集群之间的通信无关
  # 例如：你希望公网和内网都能支持访问，就可能会设置多个IP
  certSANs:
    - 192.168.103.231                              # 内网IP
    - 123.177.22.26                                # 外网IP
    - dev-share.top                                # 域名
  # 这种做法起到的效果是，使用192.168.103.231、123.177.22.26、dev-share.top生成的证书都可以访问ApiServer

# 配置集群内部网段
networking:
  dnsDomain: cluster.local
  serviceSubnet: 10.96.0.0/16                      # 设定service 网段，不做修改
  podSubnet: 10.244.0.0/16                         # 设定pod 网段

---

apiVersion: kubelet.config.k8s.io/v1beta1
kind: KubeletConfiguration
cgroupDriver: systemd
# END ANSIBLE MANAGED BLOCK

```

* * *

* * *

* * *

###### **`.kube/config`文件属性解释**

```ruby
apiVersion: v1
clusters:                                   # 多集群配置
- cluster:                                  # 加入一个集群
    certificate-authority-data:             # 集群的证书
    server: https://192.168.20.94:6443      # 集群api-server地址
  name: kubernetes                          # 集群名称

contexts:                                   # 上下文件配置
- context:                                  # 加入一个上下文
    cluster: kubernetes                     # 建立上下文与集群的关系
    user: kubernetes-admin                  # 建立上下文与集群用户的关系
  name: cluster01-dhc-local                 # 上下文名称(通过上下文切换集群时使用)

current-context: cluster01-dhc-local        # 指定当前正在使用的上下文

kind: Config                                # 集群用户信息配置
preferences: {}
users:
- name: kubernetes-admin                    # 指定集群用户名
  user:
    client-certificate-data:                # 集群用户的证书文件
    client-key-data:                        # 集群用户的证书文件

```

* * *

###### 集群1 配置文件

```ruby
[root@master01 ~]# cat /home/cluster01/config
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: 内容省略
    server: https://192.168.20.94:6443
  name: dhc-local

contexts:
- context:
    cluster: dhc-local
    user: kubernetes-admin
  name: cluster_01

current-context: cluster_01

kind: Config
preferences: {}
users:
- name: kubernetes-admin
  user:
    client-certificate-data: 内容省略
    client-key-data: 内容省略

[root@master01 ~]#

```

* * *

###### 集群2 配置文件

```ruby
[root@master01 ~]# cat /home/cluster02/config
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: 内容省略
    server: https://39.104.94.107:6443
  name: aliyun-cluster

contexts:
- context:
    cluster: aliyun-cluster
    user: Eric.Mao
  name: cluster_02

current-context: cluster_02

kind: Config
preferences: {}
users:
- name: Eric.Mao
  user:
    client-certificate-data: 内容省略
    client-key-data: 内容省略

[root@master01 ~]#
```

* * *

###### 环境变量配置

```ruby
# 指定 集群1 的配置文件
export CLUSTER_01=/home/cluster01/config
# 指定 集群2 的配置文件
export CLUSTER_02=/home/cluster02/config
# 指定k8s鉴权配置文件(注： 这里是通过kubectl自动为我们生成context)
export KUBECONFIG=$CLUSTER_01:$CLUSTER_02
```

* * *

###### 查看kubectl自动合并的 config文件

```ruby
[root@master01 ~]# kubectl config view
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: DATA+OMITTED
    server: https://39.104.94.107:6443
  name: aliyun-cluster
- cluster:
    certificate-authority-data: DATA+OMITTED
    server: https://192.168.20.94:6443
  name: dhc-local

contexts:
- context:
    cluster: dhc-local
    user: kubernetes-admin
  name: cluster_01
- context:
    cluster: aliyun-cluster
    user: Eric.Mao
  name: cluster_02

current-context: cluster_02

kind: Config
preferences: {}
users:
- name: Eric.Mao
  user:
    client-certificate-data: REDACTED
    client-key-data: REDACTED
- name: kubernetes-admin
  user:
    client-certificate-data: REDACTED
    client-key-data: REDACTED
[root@master01 ~]#

```

* * *

###### 查询当前使用的 context

```ruby
[root@master01 ~]# kubectl config get-contexts
当前使用   上下文名称      集群名称           集群用户名            所属命名空间
CURRENT   NAME           CLUSTER            AUTHINFO             NAMESPACE
          cluster_01     dhc-local          kubernetes-admin
*         cluster_02     aliyun-cluster     Eric.Mao
[root@master01 ~]#

```

* * *

###### 切换默认上下文

```ruby
kubectl config use-context cluster_01
```

* * *

###### 使用上下文进行集群切换

```ruby
kubectl --context cluster_02 get nodes
kubectl --context cluster_01 get nodes
```

* * *

* * *

* * *

* * *

* * *

* * *

###### 如果要重新创建 .kube/config 文件 (K8S Version: 1.16.6)

###### 用脚本的方式实现

**create\_kube.sh**

```shell
#!/bin/bash
# 设定集群名称，随便写，k8s集群中有没有都可以
CLUSTER_NAME='aliyun-cluster'
# 真实的 集群中的 apiserver地址
API_SERVER='https://39.104.94.107:6443'
# 最后生成的文件，名称随便写
KUBE_CONFIG='./kubeconfig'
# 上下文名称，名称随便写
CONTEXT_NAME='cluster_02'
# 用户名称，名称随便写
USERNAME='Eric.Mao'

# 如果生成的文件以存在，就把它删除
rm -rf ${KUBE_CONFIG}

# 生成集群签证
kubectl config set-cluster ${CLUSTER_NAME} \
    --certificate-authority=/etc/kubernetes/pki/ca.crt \
    --embed-certs=true \
    --server=${API_SERVER} \
    --kubeconfig=${KUBE_CONFIG}

# 生成上下文
kubectl config set-context ${CONTEXT_NAME} \
    --cluster=${CLUSTER_NAME} \
    --user=${USERNAME} \
    --kubeconfig=${KUBE_CONFIG}

# 生成用户签证
kubectl config set-credentials ${USERNAME} \
    --client-certificate=/etc/kubernetes/pki/apiserver-kubelet-client.crt \
    --embed-certs=true \
    --client-key=/etc/kubernetes/pki/apiserver-kubelet-client.key \
    --kubeconfig=${KUBE_CONFIG}

# 应用默认上下文
kubectl config use-context ${CONTEXT_NAME} \
    --kubeconfig=${KUBE_CONFIG}

```

* * *

###### 说明

```ruby
# 生成集群签证
kubectl config set-cluster cluster_02 \
    --certificate-authority=/etc/kubernetes/pki/ca.crt \
    --embed-certs=true \
    --server=https://39.104.94.107:6443 \
    --kubeconfig=kubeconfig

# 生成用户签证
kubectl config set-credentials eric.mao \
    --client-certificate=/etc/kubernetes/pki/apiserver-kubelet-client.crt \
    --embed-certs=true \
    --client-key=/etc/kubernetes/pki/apiserver-kubelet-client.key \
    --kubeconfig=kubeconfig

# 生成上下文
kubectl config set-context cluster_02 \
    --cluster=aliyun-cluster \
    --user=eric.mao \
    --kubeconfig=kubeconfig

# 应用默认上下文
kubectl config use-context cluster_02 \
    --kubeconfig=kubeconfig

```

* * *

* * *

* * *

* * *

* * *

* * *

###### 在主控机，批量添加远程集群 `generate-kube-config.sh`

```shell
#!/bin/bash
:<< EOF
测试：
./generate-kube-config.sh \
    cluster_01=192.168.103.230 \
    cluster_02=192.168.103.233 \
    cluster_03=192.168.103.236 \
    && source /etc/profile
EOF

env='export KUBECONFIG='
# 循环打印所有传入的参数
for i in "$@"; do
    if [ -n "$i" ]; then
        array=(${i//=/ })
        # 设定集群名称，随便写，k8s集群中有没有都可以
        CLUSTER_NAME="${array[0]}"
        # 真实的 集群中的 apiserver地址
        API_SERVER="https://${array[1]}:6443"
        # 最后生成的文件，名称随便写
        KUBE_CONFIG="${array[0]}"
        # 上下文名称，名称随便写
        CONTEXT_NAME="${array[0]}"
        # 环境变量名称，名称随便写
        CONTEXT_NAME_ENV=$( echo $CONTEXT_NAME | tr 'a-z' 'A-Z' | tr '-' '_')
        # 用户名称，名称随便写
        USERNAME="${array[0]}"

        # 如果生成的文件以存在，就把它删除
        rm -rf "./${KUBE_CONFIG}"


        echo
        echo
        echo -e "\033[35m==========================\033[0m"
        echo -e "\033[36m 在远程-生成集群签证 \033[0m"
        ssh ${array[1]} kubectl config set-cluster ${CLUSTER_NAME} \
            --certificate-authority=/etc/kubernetes/pki/ca.crt \
            --embed-certs=true \
            --server=${API_SERVER} \
            --kubeconfig="./${KUBE_CONFIG}"


        echo +------------------------+
        echo -e "\033[36m 在远程-生成上下文 \033[0m"
        ssh ${array[1]} kubectl config set-context ${CONTEXT_NAME} \
            --cluster=${CLUSTER_NAME} \
            --user=${USERNAME} \
            --kubeconfig="./${KUBE_CONFIG}"


        echo +------------------------+
        echo -e "\033[36m 在远程-生成用户签证 \033[0m"
        ssh ${array[1]} kubectl config set-credentials ${USERNAME} \
            --client-certificate=/etc/kubernetes/pki/apiserver-kubelet-client.crt \
            --embed-certs=true \
            --client-key=/etc/kubernetes/pki/apiserver-kubelet-client.key \
            --kubeconfig="./${KUBE_CONFIG}"


        echo +------------------------+
        echo -e "\033[36m 将远程-用户签证拉取到本地 \033[0m"
        scp ${array[1]}:~/${KUBE_CONFIG} ./${KUBE_CONFIG}


        echo +------------------------+
        echo -e "\033[36m 应用默认上下文 \033[0m"
        kubectl config use-context ${CONTEXT_NAME} \
            --kubeconfig="./${KUBE_CONFIG}"


        # 删除旧的环境变量
        sed -i /"export $CONTEXT_NAME_ENV=*"/d /etc/profile
        # 新增环境变量
        echo "export $CONTEXT_NAME_ENV=$PWD/$CONTEXT_NAME" >> /etc/profile


        # 累计拼接多个上下文件的环境变量
        env+="\$$CONTEXT_NAME_ENV:"


        echo -e "\033[35m==========================\033[0m"
        echo
        echo

    fi
done

# 删除旧的环境变量
sed -i /"export KUBECONFIG=*"/d /etc/profile

# 将最后一个字符去掉，并写入到环境变量
echo ${env%?} >> /etc/profile

```

* * *

##### 查询集群列表

```ruby
source /etc/profile

kubectl config get-contexts

```

* * *

* * *

* * *
