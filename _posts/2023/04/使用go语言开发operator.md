---
title: "使用Go语言开发Operator"
date: "2023-04-13"
categories: 
  - "k8s"
---

## 使用Go语言开发Operator

> - 使用Go语言开发Operator，实际上就是使用 Client-go库进行封装
> - 一开始会想要如何获取kubernetes中的操作权限呢？
>     - 在开发 Operator 时，只需要在部署 Operator 的 Pod 文件中指定 ServiceAccount，就可以使用 Client-go 库进行封装，而不必再次考虑身份验证和授权的问题。
>     - 具体来说，Kubernetes 提供了 ServiceAccount 来管理 Pod 的认证信息，并且会自动为每个 Pod 创建一个默认的 ServiceAccount（默认名称为 default），如果没有显式指定，则使用该 ServiceAccount。
>     - 在通过 Kubernetes 的 Deployment 部署 Operator 时，我们可以通过为 Pod 指定 ServiceAccount 如： Pod 的 spec 中添加 serviceAccountName 字段。

* * *

## 封装个工具类 logger.go

```go
package logger

import (
    "fmt"
    "log"
    "os"
)

const (
    Reset  = "\033[0m"
    Black  = "\033[30m"
    Red    = "\033[31m"
    Green  = "\033[32m"
    Yellow = "\033[33m"
    Blue   = "\033[34m"
    Purple = "\033[35m"
    Cyan   = "\033[36m"
    White  = "\033[37m"

    Bold       = "\033[1m"
    Underline  = "\033[4m"
    Background = "\033[7m"
)

type LogLevel int

const (
    LogError LogLevel = iota
    LogInfo
    LogWarning
    LogDebug
)

var LogLevelNames = []string{"ERROR", "INFO", "WARNING", "DEBUG"}

var logLevel LogLevel

func init() {
    // TODO: 设置日志工具级别
    os.Setenv("LOG_LEVEL", "DEBUG")
    setLogLevelFromEnv()
}

func setLogLevel(level LogLevel) {
    logLevel = level
}

func setLogLevelFromEnv() {
    logLevelStr := os.Getenv("LOG_LEVEL")
    if logLevelStr == "" {
        setLogLevel(LogInfo)
        return
    }
    switch logLevelStr {
    case "ERROR":
        setLogLevel(LogError)
    case "INFO":
        setLogLevel(LogInfo)
    case "WARNING":
        setLogLevel(LogWarning)
    case "DEBUG":
        setLogLevel(LogDebug)
    default:
        setLogLevel(LogInfo)
    }
}

func logf(color string, level LogLevel, format string, v ...interface{}) {
    if level <= logLevel {
        message := fmt.Sprintf(format, v...)
        log.Printf("[%s%s%s] %s%s%s\n", color, LogLevelNames[level], Reset, color, message, Reset)
    }
}

// Error 打印错误日志
func Error(v ...interface{}) {
    logf(Red, LogError, "%v", v...)
}

// Errorf 格式化打印错误日志
func Errorf(format string, v ...interface{}) {
    logf(Red, LogError, format, v...)
}

// Info 打印信息日志
func Info(v ...interface{}) {
    logf(Green, LogInfo, "%v", v...)
}

// Infof 格式化打印信息日志
func Infof(format string, v ...interface{}) {
    logf(Green, LogInfo, format, v...)
}

// Warning 打印警告日志
func Warning(v ...interface{}) {
    logf(Yellow, LogWarning, "%v", v...)
}

// Warningf 格式化打印警告日志
func Warningf(format string, v ...interface{}) {
    logf(Yellow, LogWarning, format, v...)
}

// Debug 打印调试日志
func Debug(v ...interface{}) {
    logf(Cyan, LogDebug, "%v", v...)
}

// Debugf 格式化打印调试日志
func Debugf(format string, v ...interface{}) {
    logf(Cyan, LogDebug, format, v...)
}

```

## 程序源代码 main.go

```go
package main

import (
    "context"
    "github.com/lemonit-eric-mao/commons/logger"
    "fmt"
    "github.com/google/uuid"
    v1 "k8s.io/api/core/v1"
    metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
    "k8s.io/client-go/kubernetes"
    "k8s.io/client-go/rest"
    "k8s.io/client-go/tools/clientcmd"
    "k8s.io/client-go/util/retry"
    "os"
    "time"
)

func main() {

    // 创建一个 Kubernetes 客户端。
    restConfig, err := clientcmd.BuildConfigFromFlags("", "")
    if err != nil {
        restConfig, err = rest.InClusterConfig()
        if err != nil {
            panic(err)
        }
    }

    // 可以把 clientset 理解为 kubectl
    clientset, err := kubernetes.NewForConfig(restConfig)
    if err != nil {
        panic(err)
    }
    logger.Debug("客户创建成功。")

    // -----------------------------------------------------------------------------------------------------------------

    // 获取当前 Pod 所在的命名空间。
    // 这是一种常用的获取当前 Pod 所在命名空间的方法，也是比较标准的方法之一。
    namespaceBytes, err := os.ReadFile("/var/run/secrets/kubernetes.io/serviceaccount/namespace")
    if err != nil {
        panic(err)
    }
    namespace := string(namespaceBytes)
    logger.Debugf("获得当前命名空间 --> %s。", namespace)

    // -----------------------------------------------------------------------------------------------------------------

    // 创建 Pod。
    // 1. 编辑Pod模板
    podName := fmt.Sprintf("flexi-build-pod-%s", uuid.New().String()[:8])
    pod := &v1.Pod{
        ObjectMeta: metav1.ObjectMeta{
            Name:      podName,
            Namespace: namespace,
        },
        Spec: v1.PodSpec{
            InitContainers: []v1.Container{
                {
                    Name:  fmt.Sprintf("%s-init-container", podName),
                    Image: "busybox",
                    Command: []string{
                        "/bin/sh",
                        "-c",
                        "echo Init Container running && sleep 3",
                    },
                    VolumeMounts: []v1.VolumeMount{
                        {
                            Name:      "shared-data",
                            MountPath: "/init-data",
                        },
                    },
                },
            },
            Containers: []v1.Container{
                {
                    Name:  fmt.Sprintf("%s-container", podName),
                    Image: "nginx:1.21.1",
                    Env: []v1.EnvVar{
                        {
                            Name:  "MY_ENV_VAR1",
                            Value: "env-var-1-value",
                        },
                        //{
                        //    Name:      "MY_ENV_VAR2",
                        //    ValueFrom: &v1.EnvVarSource{SecretKeyRef: &v1.SecretKeySelector{Key: "password", LocalObjectReference: v1.LocalObjectReference{Name: "my-secret"}}},
                        //},
                    },
                    VolumeMounts: []v1.VolumeMount{
                        {
                            Name:      "shared-data",
                            MountPath: "/init-data",
                        },
                    },
                },
            },
            Volumes: []v1.Volume{
                {
                    Name: "shared-data",
                    VolumeSource: v1.VolumeSource{
                        EmptyDir: &v1.EmptyDirVolumeSource{},
                    },
                },
            },
        },
    }
    // 2. 执行创建
    logger.Debugf("创建Pod --> %s。", podName)
    _, err = clientset.CoreV1().Pods(namespace).Create(context.Background(), pod, metav1.CreateOptions{})
    if err != nil {
        panic(err)
    }

    // 查看 Pod 创建结果。
    retryErr := retry.OnError(
        retry.DefaultRetry,
        func(err error) bool { return true },
        func() error {
            pod, err = clientset.CoreV1().Pods(namespace).Get(context.Background(), podName, metav1.GetOptions{})
            return err
        },
    )
    if retryErr != nil {
        panic(retryErr)
    }

    // -----------------------------------------------------------------------------------------------------------------

    // 删除 Pod。
    time.Sleep(30e9)
    logger.Debugf("删除Pod --> %s。", pod.Name)
    err = clientset.CoreV1().Pods(namespace).Delete(context.Background(), podName, metav1.DeleteOptions{})
    if err != nil {
        panic(err)
    }

    // -----------------------------------------------------------------------------------------------------------------

}

```

* * *

## **[项目地址](https://gitee.com/eric-mao/flexi-build-operator.git)**
