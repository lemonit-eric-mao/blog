---
title: 'containerd 常用命令'
date: '2021-03-20T01:55:45+00:00'
status: publish
permalink: /2021/03/20/containerd-%e5%b8%b8%e7%94%a8%e5%91%bd%e4%bb%a4
author: 毛巳煜
excerpt: ''
type: post
id: 7052
category:
    - containerd
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
---
###### 常用命令

- **ctr**： 是containerd本身的CLI

```shell
[root@master01 ~]# ctr -h
NAME:
   ctr -
        __
  _____/ /______
 / ___/ __/ ___/
/ /__/ /_/ /
\___/\__/_/

containerd CLI


USAGE:
   ctr [global options] command [command options] [arguments...]

VERSION:
   1.4.4

DESCRIPTION:

ctr is an unsupported debug and administrative client for interacting
with the containerd daemon. Because it is unsupported, the commands,
options, and operations are not guaranteed to be backward compatible or
stable from release to release of the containerd project.

COMMANDS:
   plugins, plugin            provides information about containerd plugins
   version                    print the client and server versions
   containers, c, container   manage containers
   content                    manage content
   events, event              display containerd events
   images, image, i           manage images
   leases                     manage leases
   namespaces, namespace, ns  manage namespaces
   pprof                      provide golang pprof outputs for containerd
   run                        run a container
   snapshots, snapshot        manage snapshots
   tasks, t, task             manage tasks
   install                    install a new package
   oci                        OCI tools
   shim                       interact with a shim directly
   help, h                    Shows a list of commands or help for one command

GLOBAL OPTIONS:
   --debug                      enable debug output in logs
   --address value, -a value    address for containerd's GRPC server (default: "/run/containerd/containerd.sock") [<span class="katex math inline">CONTAINERD_ADDRESS]
   --timeout value              total timeout for ctr commands (default: 0s)
   --connect-timeout value      timeout for connecting to containerd (default: 0s)
   --namespace value, -n value  namespace to use with commands (default: "default") [</span>CONTAINERD_NAMESPACE]
   --help, -h                   show help
   --version, -v                print the version

# -------------------------------------------------------------------


```

```shell
[root@master01 ~]# ctr i -h
NAME:
   ctr images - manage images

USAGE:
   ctr images command [command options] [arguments...]

COMMANDS:
   check       check that an image has all content available locally
   export      export images
   import      import images
   list, ls    list images known to containerd
   mount       mount an image to a target path
   unmount     unmount the image from the target
   pull        pull an image from a remote
   push        push an image to a remote
   remove, rm  remove one or more images by reference
   tag         tag an image
   label       set and clear labels for an image

OPTIONS:
   --help, -h  show help

```

```shell
[root@master01 ~]# ctr i pull -h
NAME:
   ctr images pull - pull an image from a remote

USAGE:
   ctr images pull [command options] [flags] <ref>

DESCRIPTION:
   Fetch and prepare an image for use in containerd.

After pulling an image, it should be ready to use the same reference in a run
command. As part of this process, we do the following:

1. Fetch all resources into containerd.
2. Prepare the snapshot filesystem with the pulled resources.
3. Register metadata for the image.


OPTIONS:
   --skip-verify, -k       skip SSL certificate validation
   --plain-http            allow connections using plain HTTP
   --user value, -u value  user[:password] Registry user and password
   --refresh value         refresh token for authorization server
   --hosts-dir value       Custom hosts configuration directory
   --tlscacert value       path to TLS root CA
   --tlscert value         path to TLS client certificate
   --tlskey value          path to TLS client key
   --snapshotter value     snapshotter name. Empty value stands for the default value. [$CONTAINERD_SNAPSHOTTER]
   --label value           labels to attach to the image
   --platform value        Pull content from a specific platform
   --all-platforms         pull content and metadata from all platforms
   --all-metadata          Pull metadata for all platforms

</ref>
```

- - - - - -

###### 导入镜像

`ctr -n 命名空间 image import 镜像文件包.tar`

```ruby
ctr -n k8s.io image import {{ deploy_dir }}/images/k8s-{{K8sVersion}}.tar

```

- - - - - -

###### 导出镜像

`ctr -n 命名空间 image export 镜像文件包.tar 镜像名:tag 镜像名:tag ....:..`

```ruby
ctr -n k8s.io image export k8s.1.20.4.tar \
docker.io/calico/cni:v3.18.1 \
docker.io/calico/kube-controllers:v3.18.1 \
docker.io/calico/node:v3.18.1 \
docker.io/calico/pod2daemon-flexvol:v3.18.1 \
docker.io/calico/typha:v3.18.1 \
k8s.gcr.io/coredns:1.7.0 \
k8s.gcr.io/etcd:3.4.13-0 \
k8s.gcr.io/kube-apiserver:v1.20.4 \
k8s.gcr.io/kube-controller-manager:v1.20.4 \
k8s.gcr.io/kube-proxy:v1.20.4 \
k8s.gcr.io/kube-scheduler:v1.20.4 \
k8s.gcr.io/pause:3.2 \
quay.io/tigera/operator:v1.15.1

```

- - - - - -

###### 查看镜像

`ctr -n 命名空间 i ls -q`

```ruby
ctr -n k8s.io i ls -q

docker.io/calico/cni:v3.18.1
docker.io/calico/kube-controllers:v3.18.1
docker.io/calico/node:v3.18.1
docker.io/calico/pod2daemon-flexvol:v3.18.1
docker.io/calico/typha:v3.18.1
k8s.gcr.io/coredns:1.7.0
k8s.gcr.io/etcd:3.4.13-0
k8s.gcr.io/kube-apiserver:v1.20.4
k8s.gcr.io/kube-controller-manager:v1.20.4
k8s.gcr.io/kube-proxy:v1.20.4
k8s.gcr.io/kube-scheduler:v1.20.4
k8s.gcr.io/pause:3.2
quay.io/tigera/operator:v1.15.1

#--------------------------------
## 导入的镜像是由 docker save 导出的就会带有 sha256;
## 导入的镜像是由 ctr -n k8s.io image export 导出的镜像就没有 sha256;
sha256:0369cf4303ffdb467dc219990960a9baa8512a54b0ad9283eaf55bd6c0adb934
......

```

- - - - - -

###### 删除 sha256镜像， 这种镜像没有实际用处

```ruby
ctr -n k8s.io i rm $(ctr -n k8s.io i ls -q | grep 'sha256')


```

- - - - - -

- - - - - -

- - - - - -