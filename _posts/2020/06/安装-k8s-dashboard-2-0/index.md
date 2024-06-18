---
title: "安装 K8S Dashboard 2.0.0"
date: "2020-06-04"
categories: 
  - "k8s"
---

##### **`dashboard-install.sh` 编写安装脚本(复制直接用)**

```shell
cat > dashboard-install.sh << EOF

#!/bin/bash
# @Time    : 2020/01/03
# @Author  : Eric.Mao


mkdir -p /home/k8s-dashboard/yamls


################################################################################################


cat > /home/k8s-dashboard/yamls/kubernetes-dashboard.yaml << ERIC

# Copyright 2017 The Kubernetes Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

apiVersion: v1
kind: Namespace
metadata:
  name: kubernetes-dashboard

---

apiVersion: v1
kind: ServiceAccount
metadata:
  labels:
    k8s-app: kubernetes-dashboard
  name: kubernetes-dashboard
  namespace: kubernetes-dashboard

---

kind: Service
apiVersion: v1
metadata:
  labels:
    k8s-app: kubernetes-dashboard
  name: kubernetes-dashboard
  namespace: kubernetes-dashboard
spec:
  ports:
    - port: 443
      targetPort: 8443
  selector:
    k8s-app: kubernetes-dashboard

---

apiVersion: v1
kind: Secret
metadata:
  labels:
    k8s-app: kubernetes-dashboard
  name: kubernetes-dashboard-certs
  namespace: kubernetes-dashboard
type: Opaque

---

apiVersion: v1
kind: Secret
metadata:
  labels:
    k8s-app: kubernetes-dashboard
  name: kubernetes-dashboard-csrf
  namespace: kubernetes-dashboard
type: Opaque
data:
  csrf: ""

---

apiVersion: v1
kind: Secret
metadata:
  labels:
    k8s-app: kubernetes-dashboard
  name: kubernetes-dashboard-key-holder
  namespace: kubernetes-dashboard
type: Opaque

---

kind: ConfigMap
apiVersion: v1
metadata:
  labels:
    k8s-app: kubernetes-dashboard
  name: kubernetes-dashboard-settings
  namespace: kubernetes-dashboard

---

kind: Role
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  labels:
    k8s-app: kubernetes-dashboard
  name: kubernetes-dashboard
  namespace: kubernetes-dashboard
rules:
  # Allow Dashboard to get, update and delete Dashboard exclusive secrets.
  - apiGroups: [""]
    resources: ["secrets"]
    resourceNames: ["kubernetes-dashboard-key-holder", "kubernetes-dashboard-certs", "kubernetes-dashboard-csrf"]
    verbs: ["get", "update", "delete"]
    # Allow Dashboard to get and update 'kubernetes-dashboard-settings' config map.
  - apiGroups: [""]
    resources: ["configmaps"]
    resourceNames: ["kubernetes-dashboard-settings"]
    verbs: ["get", "update"]
    # Allow Dashboard to get metrics.
  - apiGroups: [""]
    resources: ["services"]
    resourceNames: ["heapster", "dashboard-metrics-scraper"]
    verbs: ["proxy"]
  - apiGroups: [""]
    resources: ["services/proxy"]
    resourceNames: ["heapster", "http:heapster:", "https:heapster:", "dashboard-metrics-scraper", "http:dashboard-metrics-scraper"]
    verbs: ["get"]

---

kind: ClusterRole
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  labels:
    k8s-app: kubernetes-dashboard
  name: kubernetes-dashboard
rules:
  # Allow Metrics Scraper to get metrics from the Metrics server
  - apiGroups: ["metrics.k8s.io"]
    resources: ["pods", "nodes"]
    verbs: ["get", "list", "watch"]

---

apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  labels:
    k8s-app: kubernetes-dashboard
  name: kubernetes-dashboard
  namespace: kubernetes-dashboard
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: kubernetes-dashboard
subjects:
  - kind: ServiceAccount
    name: kubernetes-dashboard
    namespace: kubernetes-dashboard

---

apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: kubernetes-dashboard
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: kubernetes-dashboard
subjects:
  - kind: ServiceAccount
    name: kubernetes-dashboard
    namespace: kubernetes-dashboard

---

kind: Deployment
apiVersion: apps/v1
metadata:
  labels:
    k8s-app: kubernetes-dashboard
  name: kubernetes-dashboard
  namespace: kubernetes-dashboard
spec:
  replicas: 1
  revisionHistoryLimit: 10
  selector:
    matchLabels:
      k8s-app: kubernetes-dashboard
  template:
    metadata:
      labels:
        k8s-app: kubernetes-dashboard
    spec:
      containers:
        - name: kubernetes-dashboard
          image: kubernetesui/dashboard:v2.0.0
          imagePullPolicy: Always
          ports:
            - containerPort: 8443
              protocol: TCP
          args:
            - --auto-generate-certificates
            - --namespace=kubernetes-dashboard
            # Uncomment the following line to manually specify Kubernetes API server Host
            # If not specified, Dashboard will attempt to auto discover the API server and connect
            # to it. Uncomment only if the default does not work.
            # - --apiserver-host=http://my-address:port
          volumeMounts:
            - name: kubernetes-dashboard-certs
              mountPath: /certs
              # Create on-disk volume to store exec logs
            - mountPath: /tmp
              name: tmp-volume
          livenessProbe:
            httpGet:
              scheme: HTTPS
              path: /
              port: 8443
            initialDelaySeconds: 30
            timeoutSeconds: 30
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            runAsUser: 1001
            runAsGroup: 2001
      volumes:
        - name: kubernetes-dashboard-certs
          secret:
            secretName: kubernetes-dashboard-certs
        - name: tmp-volume
          emptyDir: {}
      serviceAccountName: kubernetes-dashboard
      nodeSelector:
        "kubernetes.io/os": linux
      # Comment the following tolerations if Dashboard must not be deployed on master
      tolerations:
        - key: node-role.kubernetes.io/master
          effect: NoSchedule

---

kind: Service
apiVersion: v1
metadata:
  labels:
    k8s-app: dashboard-metrics-scraper
  name: dashboard-metrics-scraper
  namespace: kubernetes-dashboard
spec:
  ports:
    - port: 8000
      targetPort: 8000
  selector:
    k8s-app: dashboard-metrics-scraper

---

kind: Deployment
apiVersion: apps/v1
metadata:
  labels:
    k8s-app: dashboard-metrics-scraper
  name: dashboard-metrics-scraper
  namespace: kubernetes-dashboard
spec:
  replicas: 1
  revisionHistoryLimit: 10
  selector:
    matchLabels:
      k8s-app: dashboard-metrics-scraper
  template:
    metadata:
      labels:
        k8s-app: dashboard-metrics-scraper
      annotations:
        seccomp.security.alpha.kubernetes.io/pod: 'runtime/default'
    spec:
      containers:
        - name: dashboard-metrics-scraper
          image: kubernetesui/metrics-scraper:v1.0.4
          ports:
            - containerPort: 8000
              protocol: TCP
          livenessProbe:
            httpGet:
              scheme: HTTP
              path: /
              port: 8000
            initialDelaySeconds: 30
            timeoutSeconds: 30
          volumeMounts:
          - mountPath: /tmp
            name: tmp-volume
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            runAsUser: 1001
            runAsGroup: 2001
      serviceAccountName: kubernetes-dashboard
      nodeSelector:
        "kubernetes.io/os": linux
      # Comment the following tolerations if Dashboard must not be deployed on master
      tolerations:
        - key: node-role.kubernetes.io/master
          effect: NoSchedule
      volumes:
        - name: tmp-volume
          emptyDir: {}

ERIC


echo -e "\033[32m ------------------- (一)生成 kubernetes-dashboard.yaml 成功！ ------------------- \033[0m"


################################################################################################


echo -e "\033[32m ------------------- (二)创建自签名CA -------------------------------------------- \033[0m"
mkdir -p /home/k8s-dashboard/tls && cd /home/k8s-dashboard/tls

echo -e "\033[34m ................... 生成私钥 .................................................... \033[0m"
openssl genrsa -out ca.key 2048

echo -e "\033[34m ................... 生成自签名证书 .............................................. \033[0m"
openssl req -new -x509 -key ca.key -out ca.crt -days 3650 -subj "/C=CN/ST=HB/L=WH/O=DM/OU=YPT/CN=CA"


################################################################################################


echo -e "\033[32m ------------------- (三)签发dashboard证书 --------------------------------------- \033[0m"

echo -e "\033[34m ................... 生成私钥 .................................................... \033[0m"
openssl genrsa -out dashboard.key 2048

echo -e "\033[34m ................... 申请签名 .................................................... \033[0m"
openssl req -new -sha256 -key dashboard.key -out dashboard.csr -subj "/C=CN/ST=HB/L=WH/O=DM/OU=YPT/CN=kubernetes-dashboard"

echo -e "\033[34m ................... 签发证书 .................................................... \033[0m"
openssl x509 -req -sha256 -days 3650 -in dashboard.csr -out dashboard.crt -CA ca.crt -CAkey ca.key -CAcreateserial


################################################################################################


echo -e "\033[32m ------------------- (四)生成 p12证书 ---------------------------------------------- \033[0m"
grep 'client-certificate-data' ~/.kube/config | head -n 1 | awk '{print \$2}' | base64 -d > kubecfg.crt
grep 'client-key-data' ~/.kube/config | head -n 1 | awk '{print \$2}' | base64 -d > kubecfg.key
openssl pkcs12 -export -clcerts -inkey kubecfg.key -in kubecfg.crt -out kubecfg.p12 -name "kubernetes-client"


################################################################################################


echo -e "\033[32m ------------------- (五)挂载证书到dashboard ------------------------------------- \033[0m"

kubectl create secret generic kubernetes-dashboard-certs --from-file="/home/k8s-dashboard/tls/dashboard.crt,/home/k8s-dashboard/tls/dashboard.key" -n kubernetes-dashboard


################################################################################################


echo -e "\033[32m ------------------- (六)启动dashboard ------------------------------------------- \033[0m"
kubectl apply -f /home/k8s-dashboard/yamls/


################################################################################################


echo -e "\033[32m ------------------- (七)获取 token ---------------------------------------------- \033[0m"
echo -e "\033[36m \$(kubectl describe secret kubernetes-dashboard -n kubernetes-dashboard | grep token:) \033[0m"


################################################################################################


echo -e "\033[32m ------------------- (End)测试地址 ----------------------------------------------- \033[0m"
echo -e "\033[36m \$(kubectl cluster-info | grep 'Kubernetes' | awk '/http/ {print \$NF}')/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/ \033[0m"
echo -e "\033[36m kubectl get svc -A -o wide | grep kubernetes-dashboard \033[0m"
echo -e "\033[36m kubectl get pod -A -o wide | grep kubernetes-dashboard \033[0m"
echo -e "\033[36m 证书文件目录: /home/k8s-dashboard/tls/kubecfg.p12 \033[0m"
echo -e "\033[36m Yaml文件目录: /home/k8s-dashboard/yamls/ \033[0m"

EOF

```

* * *

##### 编写卸载脚本 dashboard-uninstall.sh

```shell
cat > dashboard-uninstall.sh << EOF

#!/bin/bash
# @Time    : 2020/01/03
# @Author  : Eric.Mao

read -p "是否删除Dashboard [y/N]: " IP
if [ "\$IP" != 'y' ]; then
    echo -e "\033[31m 退出程序. \033[0m"
    exit
fi

kubectl delete -f /home/k8s-dashboard/yamls/
kubectl delete secret kubernetes-dashboard-certs -n kubernetes-dashboard
rm -rf /home/k8s-dashboard/

EOF

```

* * *

* * *

* * *
