---
title: "Golang 1.20 集成 Helm v3 SDK 开发"
date: "2023-07-03"
categories: 
  - "go语言"
  - "helm"
---

## 最基本的Helm Chart安装与删除

### main.go

> Golang `-->` Helm.v3 SDK `-->` Operator连接远程Helm Chart仓库 `-->` Operator将远程Chart包缓存到本地操作系统 `-->` Operator使用Helm SDK加载本地Chart包到Operator中 `-->` Operator将Chart包中应用程序部署到Kubernetes中

```go
package main

import (
    "app-factory-operator/commons/logger"
    "helm.sh/helm/v3/pkg/action"
    "helm.sh/helm/v3/pkg/chart/loader"
    "helm.sh/helm/v3/pkg/cli"
    "os"
)

/**
 * Helm v3 的 SDK 提供了自己的一套 API 和方法来管理 Helm Charts 和与 Kubernetes 集群进行交互。
 * 这些方法封装了与 Kubernetes API 通信的细节，使您能够通过 Helm SDK 直接操作 Kubernetes 集群，而无需直接使用 client-go 包。
 */
func main() {
    // 安装Helm Chart
    installHelmChart()
    // 卸载Helm Chart
    unInstallHelmChart()
}

// 安装Helm Chart
/**
 * 相当于: helm install
 */
func installHelmChart() {

    // 第一步: 配置仓库、Chart的信息
    logger.Debug("第一步: 配置仓库、Chart的信息")
    var repoURL, chartName, chartVersion, namespace, releaseName string
    repoURL = "https://charts.bitnami.com/bitnami" // 仓库地址
    chartName = "nginx"                            // Chart名称
    chartVersion = "13.2.34"                       // Chart版本
    namespace = "default111"                       // 命名空间
    releaseName = "nginx-test"                     // 在kubernetes中的程序名

    // 第二步: 获得 Helm 的 SDK
    logger.Debug("第二步: 获得 Helm 的 SDK")
    settings := cli.New()

    // 第三步: 初始化 action 配置
    logger.Debug("第三步: 初始化action")
    actionConfig := new(action.Configuration)
    if err := actionConfig.Init(settings.RESTClientGetter(), namespace, os.Getenv("HELM_DRIVER"), logger.Debugf); err != nil {
        logger.Errorf("第三步: 初始化 action 失败\n%s", err)
        os.Exit(1)
        return
    }

    // 第四步: 安装Chart前准备
    logger.Debug("第四步: 安装Chart前准备")
    install := action.NewInstall(actionConfig)
    install.RepoURL = repoURL
    install.Version = chartVersion
    install.Timeout = 3 * time.Minute // 等待程序启动，3分钟后判断定超时
    install.CreateNamespace = true
    install.Wait = true
    // kubernetes 中的配置
    install.Namespace = namespace
    install.ReleaseName = releaseName

    // 第五步: 将远程仓库中的Chart包下载到默认的缓存目录中（~/.cache/helm/repository）
    logger.Debug("第五步: 将远程仓库中的Chart包下载到默认的缓存目录中")
    chartRequested, err := install.ChartPathOptions.LocateChart(chartName, settings)
    if err != nil {
        logger.Errorf("第五步: 下载失败\n%s", err)
        return
    }

    // 第六步: 加载缓存目录中的Chart包
    logger.Debug("第六步: 加载缓存目录中的Chart包")
    chart, err := loader.Load(chartRequested)
    if err != nil {
        logger.Errorf("第六步: 加载失败\n%s", err)
        return
    }

    // 第七步: 执行Helm安装Chart包
    logger.Debug("第七步: 执行Helm安装Chart包")
    release, err := install.Run(chart, nil)
    if err != nil {
        logger.Errorf("第七步: 执行失败\n%s", err)
        return
    }

    logger.Infof("%s 版本 %s 安装成功", release.Name, release.Chart.Metadata.Version)
}

// 卸载Helm Chart
/**
 * 相当于: helm uninstall
 */
func unInstallHelmChart() {

    // 第一步: 配置卸载信息
    logger.Debug("第一步: 配置卸载信息")
    var namespace, releaseName string
    namespace = "default111"   // 命名空间
    releaseName = "nginx-test" // 在kubernetes中的程序名

    // 第二步: 获得 Helm 的 SDK
    logger.Debug("第二步: 获得 Helm 的 SDK")
    settings := cli.New()

    // 第三步: 初始化 action 配置
    logger.Debug("第三步: 初始化action")
    actionConfig := new(action.Configuration)
    if err := actionConfig.Init(settings.RESTClientGetter(), namespace, os.Getenv("HELM_DRIVER"), logger.Debugf); err != nil {
        logger.Errorf("第三步: 初始化失败\n%s", err)
        os.Exit(1)
    }

    // 第四步: 卸载Chart前准备
    logger.Debug("第四步: 卸载Chart前准备")
    uninstall := action.NewUninstall(actionConfig)
    uninstall.Timeout = 3 * time.Minute // 等待程序停止，3分钟后判断定超时
    uninstall.KeepHistory = false

    // 第五步: 开始卸载
    logger.Debug("第五步: 开始卸载")
    resp, err := uninstall.Run(releaseName)
    if err == nil && resp != nil && resp.Release != nil {
        logger.Infof("%s 成功卸载\n", resp.Release.Name)
    } else {
        logger.Errorf("卸载失败\n%s", err)
    }

}

```

### Helm Chart仓库的 增、删、查

#### chartRepository.go

```go
package kubestore

import (
    "helm.sh/helm/v3/pkg/cli"
    "helm.sh/helm/v3/pkg/repo"
    "kube-store-operator/commons/logger"
)

// 添加一个仓库地址
// Helm 的添加仓库地就是将【仓库名+仓库地址】写到一个本地的repositories.yaml文件中
/**
 * 相当于: helm repo add 仓库名 https://xxx.com
 */
func add() error {

    // 创建一个 Entry 结构体，表示仓库的配置信息
    entry := &repo.Entry{
        Name:     "bitnami",
        URL:      "https://charts.bitnami.com/bitnami",
        Username: "myusername",
        Password: "mypassword",
    }

    settings := cli.New()

    // {
    //     "settings": {
    //         "RegistryConfig": "/root/.config/helm/registry/config.json",
    //         "RepositoryConfig": "/root/.config/helm/repositories.yaml",
    //         "RepositoryCache": "/root/.cache/helm/repository",
    //         "PluginsDirectory": "/root/.local/share/helm/plugins"
    //         ......
    //     }
    // }
    // 获取仓库配置文件路径 repoFile = os.Getenv("HOME") + "/.config/helm/repositories.yaml"
    repoFile := settings.RepositoryConfig

    // 加载仓库配置文件
    repositories, err := repo.LoadFile(repoFile)
    // 如果文件不存在
    if err != nil {
        // 创建一个新的仓库配置对象
        repositories = repo.NewFile()
    }

    // 检查要添加的仓库是否已存在
    if repositories.Has(entry.Name) {
        return fmt.Errorf("仓库 %s 已存在", entry.Name)
    }

    // 添加仓库信息到仓库配置
    repositories.Add(entry)

    // 保存更新后的仓库配置到文件
    if err = repositories.WriteFile(repoFile, 0644); err != nil {
        return fmt.Errorf("无法保存仓库配置文件：%s", err)
    }

    logger.Debugf("成功添加仓库地址：%s。", entry.Name)
    return nil
}

// 查看仓库信息
/**
 * 相当于: helm repo list
 */
func list() {

    // 使用 helm.Settings 获取 Helm 配置文件路径
    settings := cli.New()

    // 加载仓库配置文件
    repositories, err := repo.LoadFile(settings.RepositoryConfig)
    if err != nil {
        logger.Errorf("无法加载仓库配置文件：%s", err)
        return
    }

    // 获取所有配置的仓库名称
    for _, repo := range repositories.Repositories {
        logger.Debugf("%s \t\t %s", repo.Name, repo.URL)
    }

}

// 删除一个仓库地址
/**
 * 相当于: helm repo remove 仓库名
 */
func remove(repoName string) {
    settings := cli.New()

    // 获取仓库配置文件路径
    repoFile := settings.RepositoryConfig

    // 加载仓库配置文件
    repositories, err := repo.LoadFile(repoFile)
    if err != nil {
        logger.Errorf("无法加载仓库配置文件：%s", err)
        return
    }

    // 检查要删除的仓库是否存在
    if !repositories.Has(repoName) {
        logger.Warningf("仓库 %s 不存在", repoName)
        return
    }

    // 从仓库配置中删除仓库
    repositories.Remove(repoName)

    // 保存更新后的仓库配置到文件
    if err := repositories.WriteFile(repoFile, 0644); err != nil {
        logger.Errorf("无法保存仓库配置文件：%s", err)
        return
    }

    logger.Debugf("删除仓库 %s 成功。", repoName)
}


// 更新仓库的Helm Chart仓库
/**
 * 相当于:
 [root@centos-01 (19:25:15) ~]
 └─# helm repo update
 Hang tight while we grab the latest from your chart repositories...
 ...Successfully got an update from the "ingress-nginx" chart repository
 ...Successfully got an update from the "netdata" chart repository
 ...Successfully got an update from the "bitnami" chart repository
 Update Complete. ⎈Happy Helming!⎈
 */
func update() (string, error) {
    settings := cli.New()
    // 加载仓库配置文件
    repositories, err := repo.LoadFile(settings.RepositoryConfig)
    if err != nil {
        return "", fmt.Errorf("无法加载仓库配置文件：%s", err)
    }

    // 遍历每个仓库
    for _, repoEntry := range repositories.Repositories {
        // 添加要检索的仓库
        chartRepository, err := repo.NewChartRepository(repoEntry, getter.All(settings))
        if err != nil {
            return "", fmt.Errorf("无法添加仓库：%s\n", err)
        }

        // 更新仓库索引信息
        if _, err := chartRepository.DownloadIndexFile(); err != nil {
            return "", fmt.Errorf("无法下载仓库索引：%s\n", err)
        }

        logger.Debugf("...Successfully got an update from the %s chart repository", repoEntry.Name)
    }

    return "Update Complete. ⎈Happy Helming!⎈", nil
}

```

* * *

* * *

* * *

## 实战封装

### 设计思路

> ```go
> // 设计思路都在这里，SDK的集成主要是不改变Helm Cli的使用习惯，并以代码的方式实现，具体步骤如下：
> func Router() {
>     // 操作Chart仓库
>     http.HandleFunc("/repo/add", handleAddRepo)       // 1. 添加一个Chart仓库
>     http.HandleFunc("/repo/list", handleListRepos)    // 2. 查看是否添加成功
>     http.HandleFunc("/repo/remove", handleRemoveRepo) // 2.1 添加错了可以删除掉
>     http.HandleFunc("/repo/update", handleUpdateRepo) // 3. 根据仓库的repositories.yaml配置文件信息更新索引文件
> 
>     // 操作Chart包
>     http.HandleFunc("/search/repo", handleSearchRepo) // 4. 查询仓库中最新的Chart包信息
>     http.HandleFunc("/search/repo/all", handleSearchAllRepo) // 4.1 查询仓库中具体Chart包的所有信息
> 
>     // 部署Chart
>     http.HandleFunc("/install", handleInstallChart)     // 5. 安装Chart应用
>     http.HandleFunc("/uninstall", handleUninstallChart) // 6. 提供了卸载功能
> }
> ```

### routers.go

```go
package kubestore

import (
    "encoding/json"
    "helm.sh/helm/v3/pkg/repo"
    "io"
    "kube-store-operator/commons/logger"
    "net/http"
)

// Router 定义路由
func Router() {
    // 操作Chart仓库
    http.HandleFunc("/repo/add", handleAddRepo)       // 相当于: helm repo add 仓库名 https://xxx.com
    http.HandleFunc("/repo/list", handleListRepos)    // 相当于: helm repo list
    http.HandleFunc("/repo/remove", handleRemoveRepo) // 相当于: helm repo remove 仓库名
    http.HandleFunc("/repo/update", handleUpdateRepo) // 相当于: helm repo update

    // 操作Chart包
    http.HandleFunc("/search/repo", handleSearchRepo)        // 相当于: helm search repo 仓库名
    http.HandleFunc("/search/repo/all", handleSearchAllRepo) // 相当于: helm search repo 仓库名 -l

    // 部署Chart
    http.HandleFunc("/install", handleInstallChart)     // 相当于: helm install
    http.HandleFunc("/uninstall", handleUninstallChart) // 相当于: helm uninstall
}

// handleAddRepo 处理添加仓库地址请求
func handleAddRepo(writer http.ResponseWriter, request *http.Request) {
    if request.Method != http.MethodPost {
        http.Error(writer, "只允许POST请求", http.StatusMethodNotAllowed)
        return
    }

    param := &repo.Entry{}
    // 解析请求数据，并转为结构体
    err := json.NewDecoder(request.Body).Decode(param)
    if err != nil {
        http.Error(writer, "解析JSON数据失败", http.StatusBadRequest)
        return
    }

    result, err := add(param)
    // 添加仓库地址
    if err != nil {
        logger.Error(err)
        http.Error(writer, err.Error(), http.StatusBadRequest)
        return
    }
    // 将返回数据转成json格式
    json.NewEncoder(writer).Encode(result)
}

// handleListRepos 处理查看仓库信息请求
func handleListRepos(writer http.ResponseWriter, request *http.Request) {
    if request.Method != http.MethodGet {
        http.Error(writer, "只允许GET请求", http.StatusMethodNotAllowed)
        return
    }

    // 查看仓库信息
    result, err := list()
    if err != nil {
        logger.Error(err)
        http.Error(writer, err.Error(), http.StatusBadRequest)
        return
    }

    json.NewEncoder(writer).Encode(result)
}

// handleRemoveRepo 处理删除仓库地址请求
func handleRemoveRepo(writer http.ResponseWriter, request *http.Request) {
    if request.Method != http.MethodDelete {
        http.Error(writer, "只允许DELETE请求", http.StatusMethodNotAllowed)
        return
    }

    param := request.FormValue("repoName")

    // 删除仓库地址
    if err := remove(param); err != nil {
        logger.Error(err)
        http.Error(writer, err.Error(), http.StatusBadRequest)
        return
    }

    writer.WriteHeader(http.StatusOK)
}

// handleUpdateRepo 处理更新仓库请求
func handleUpdateRepo(writer http.ResponseWriter, request *http.Request) {
    if request.Method != http.MethodPost {
        http.Error(writer, "只允许POST请求", http.StatusMethodNotAllowed)
        return
    }

    // 更新仓库
    result, err := update()
    if err != nil {
        logger.Error(err)
        http.Error(writer, err.Error(), http.StatusBadRequest)
        return
    }

    json.NewEncoder(writer).Encode(result)
}

// ----------------------------------------------------------------------------

// handleSearchRepo 处理查看指定仓库地址请求
func handleSearchRepo(writer http.ResponseWriter, request *http.Request) {
    if request.Method != http.MethodGet {
        http.Error(writer, "只允许GET请求", http.StatusMethodNotAllowed)
        return
    }

    repoName := request.FormValue("repoName")
    //chartName := request.FormValue("chartName")

    // 查看指定仓库地址信息
    result, err := search(repoName)
    //result, err := search(repoName, chartName)
    if err != nil {
        logger.Error(err)
        http.Error(writer, err.Error(), http.StatusBadRequest)
        return
    }

    json.NewEncoder(writer).Encode(result)
}

// handleSearchAllRepo 处理查看指定仓库地址请求
func handleSearchAllRepo(writer http.ResponseWriter, request *http.Request) {
    if request.Method != http.MethodGet {
        http.Error(writer, "只允许GET请求", http.StatusMethodNotAllowed)
        return
    }

    repoName := request.FormValue("repoName")
    chartName := request.FormValue("chartName")

    // 查看指定仓库地址信息
    result, err := searchAll(repoName, chartName)
    if err != nil {
        logger.Error(err)
        http.Error(writer, err.Error(), http.StatusBadRequest)
        return
    }

    json.NewEncoder(writer).Encode(result)
}

// ----------------------------------------------------------------------------

// handleInstallChart 处理安装Helm Chart请求
func handleInstallChart(writer http.ResponseWriter, request *http.Request) {
    if request.Method != http.MethodPost {
        http.Error(writer, "只允许POST请求", http.StatusMethodNotAllowed)
        return
    }

    param := &DeployRequest{}

    err := json.NewDecoder(request.Body).Decode(param)
    if err != nil {
        http.Error(writer, "解析JSON数据失败", http.StatusBadRequest)
        return
    }

    result, err := installChart(param)
    // 安装Helm Chart
    if err != nil {
        logger.Error(err)
        http.Error(writer, err.Error(), http.StatusBadRequest)
        return
    }

    json.NewEncoder(writer).Encode(result)
}

// handleUninstallChart 处理卸载Helm Chart请求
func handleUninstallChart(writer http.ResponseWriter, request *http.Request) {
    if request.Method != http.MethodDelete {
        http.Error(writer, "只允许DELETE请求", http.StatusMethodNotAllowed)
        return
    }

    namespace := request.FormValue("namespace")
    releaseName := request.FormValue("releaseName")

    result, err := uninstallChart(namespace, releaseName)
    // 卸载Helm Chart
    if err != nil {
        logger.Error(err)
        http.Error(writer, err.Error(), http.StatusBadRequest)
        return
    }

    json.NewEncoder(writer).Encode(result)
}

```

### chartRepository.go

```go
package kubestore

import (
    "fmt"
    "helm.sh/helm/v3/pkg/cli"
    "helm.sh/helm/v3/pkg/getter"
    "helm.sh/helm/v3/pkg/repo"
    "kube-store-operator/commons/logger"
)

// 添加一个仓库地址
// Helm 的添加仓库地就是将【仓库名+仓库地址】写到一个本地的repositories.yaml文件中
func add(entry *repo.Entry) (string, error) {
    settings := cli.New()

    repoFile := settings.RepositoryConfig

    // 加载仓库配置文件
    repositories, err := repo.LoadFile(repoFile)
    // 如果文件不存在
    if err != nil {
        // 创建一个新的仓库配置对象
        repositories = repo.NewFile()
    }

    // 检查要添加的仓库是否已存在
    if repositories.Has(entry.Name) {
        return "", fmt.Errorf("仓库 %s 已存在", entry.Name)
    }

    // 添加仓库信息到仓库配置
    repositories.Add(entry)

    // 保存更新后的仓库配置到文件
    if err = repositories.WriteFile(repoFile, 0644); err != nil {
        return "", fmt.Errorf("无法保存仓库配置文件：%s", err)
    }

    success := fmt.Sprintf("成功添加仓库地址：%s。", entry.Name)
    logger.Debug(success)
    return success, nil
}

// 查看仓库信息
func list() ([]*repo.Entry, error) {
    settings := cli.New()

    // 加载仓库配置文件
    repositories, err := repo.LoadFile(settings.RepositoryConfig)
    if err != nil {
        return nil, fmt.Errorf("无法加载仓库配置文件：%s", err)
    }
    return repositories.Repositories, nil
}

// 删除一个仓库地址
func remove(repoName string) error {
    settings := cli.New()

    repoFile := settings.RepositoryConfig

    // 加载仓库配置文件
    repositories, err := repo.LoadFile(repoFile)
    if err != nil {
        return fmt.Errorf("无法加载仓库配置文件：%s", err)
    }

    // 检查要删除的仓库是否存在
    if !repositories.Has(repoName) {
        return fmt.Errorf("仓库 %s 不存在", repoName)
    }

    // 从仓库配置中删除仓库
    result := repositories.Remove(repoName)

    // 保存更新后的仓库配置到文件
    if err = repositories.WriteFile(repoFile, 0644); err != nil || !result {
        return fmt.Errorf("无法保存仓库配置文件：%s", err)
    }

    logger.Debugf("成功删除仓库地址: %s。", repoName)
    return nil
}

// 更新仓库的Helm Chart仓库
func update() (string, error) {
    settings := cli.New()
    // 加载仓库配置文件
    repositories, err := repo.LoadFile(settings.RepositoryConfig)
    if err != nil {
        return "", fmt.Errorf("无法加载仓库配置文件：%s", err)
    }

    // 遍历每个仓库
    for _, repoEntry := range repositories.Repositories {
        // 添加要检索的仓库
        chartRepository, err := repo.NewChartRepository(repoEntry, getter.All(settings))
        if err != nil {
            return "", fmt.Errorf("无法添加仓库：%s\n", err)
        }

        // 更新仓库索引信息
        if _, err := chartRepository.DownloadIndexFile(); err != nil {
            return "", fmt.Errorf("无法下载仓库索引：%s\n", err)
        }

        logger.Debugf("...Successfully got an update from the %s chart repository", repoEntry.Name)
    }

    success := "Update Complete. ⎈Happy Helming!⎈"
    logger.Debug(success)
    return success, nil
}

```

### chartIndex.go

```go
package kubestore

import (
    "fmt"
    "helm.sh/helm/v3/pkg/cli"
    "helm.sh/helm/v3/pkg/repo"
    "kube-store-operator/commons/logger"
)

// 查看指定仓库中最新的Chart信息
// search(仓库名)
func search(repoName string) ([]*ChartListResponse, error) {
    settings := cli.New()

    path := fmt.Sprintf("%s/%s-index.yaml", settings.RepositoryCache, repoName)
    // 加载 xxx-index.yaml 文件
    indexFile, err := repo.LoadIndexFile(path)
    if err != nil {
        return nil, fmt.Errorf("仓库 %s 不存在", repoName)
    }

    var chartList []*ChartListResponse

    // 遍历指定仓库的 Chart 信息
    for _, entry := range indexFile.Entries {
        // 将每个 Chart 的最新信息提取出来
        chart := &ChartListResponse{
            ChartName:    entry[0].Name,
            ChartVersion: entry[0].Version,
            AppVersion:   entry[0].AppVersion,
            Description:  entry[0].Description,
        }
        chartList = append(chartList, chart)
    }

    // 指定仓库的Chart信息
    logger.Debugf("%s", chartList)
    return chartList, nil
}

// 查看指定仓库的Chart所有版本信息
// searchAll(仓库名, Chart名)
func searchAll(repoName, chartName string) ([]*ChartListResponse, error) {
    settings := cli.New()

    path := fmt.Sprintf("%s/%s-index.yaml", settings.RepositoryCache, repoName)
    // 加载 xxx-index.yaml 文件
    indexFile, err := repo.LoadIndexFile(path)
    if err != nil {
        return nil, fmt.Errorf("仓库 %s 不存在", repoName)
    }

    var chartList []*ChartListResponse

    // 遍历指定仓库的 Chart 信息
    for _, entry := range indexFile.Entries[chartName] {
        // 将每个 Chart 的主要信息提取出来
        chart := &ChartListResponse{
            ChartName:    entry.Name,
            ChartVersion: entry.Version,
            AppVersion:   entry.AppVersion,
            Description:  entry.Description,
        }
        chartList = append(chartList, chart)
    }

    // 指定仓库的Chart信息
    logger.Debugf("%s", chartList)
    return chartList, nil
}

```

### chart.go

```go
package kubestore

import (
    "fmt"
    "helm.sh/helm/v3/pkg/action"
    "helm.sh/helm/v3/pkg/chart/loader"
    "helm.sh/helm/v3/pkg/cli"
    "kube-store-operator/commons/logger"
    "kube-store-operator/commons/tools"
    "os"
    "time"
)

// 安装Helm Chart
func installChart(deployRequest *DeployRequest) (string, error) {

    settings := cli.New()

    actionConfig := new(action.Configuration)
    if err := actionConfig.Init(settings.RESTClientGetter(), deployRequest.Namespace, os.Getenv("HELM_DRIVER"), logger.Debugf); err != nil {
        return "", fmt.Errorf("初始化 action 失败\n%s", err)
    }

    install := action.NewInstall(actionConfig)
    install.RepoURL = deployRequest.RepoURL
    install.Version = deployRequest.ChartVersion
    install.CreateNamespace = true
    install.Wait = true
    install.Timeout = 3 * time.Minute // 等待程序启动，3分钟后判断定超时
    // kubernetes 中的配置
    install.Namespace = deployRequest.Namespace
    install.ReleaseName = deployRequest.ReleaseName

    logger.Debugf("%s Chart包开始下载。", deployRequest.ChartName)
    chartRequested, err := install.ChartPathOptions.LocateChart(deployRequest.ChartName, settings)
    if err != nil {
        return "", fmt.Errorf("下载失败\n%s", err)
    }

    chart, err := loader.Load(chartRequested)
    if err != nil {
        return "", fmt.Errorf("加载失败\n%s", err)
    }

    values, err := tools.YamlToMap(deployRequest.Values)
    if err != nil {
        return "", fmt.Errorf("Values 格式非法\n%s", err)
    }

    _, err = install.Run(chart, values)
    if err != nil {
        return "", fmt.Errorf("执行失败\n%s", err)
    }

    success := fmt.Sprintf("%s 部署成功。", deployRequest.ChartName)
    logger.Debug(success)
    return success, nil
}

// 卸载Helm Chart
func uninstallChart(namespace, releaseName string) (string, error) {

    settings := cli.New()

    actionConfig := new(action.Configuration)
    if err := actionConfig.Init(settings.RESTClientGetter(), namespace, os.Getenv("HELM_DRIVER"), logger.Debugf); err != nil {
        return "", fmt.Errorf("初始化 action 失败\n%s", err)
    }

    uninstall := action.NewUninstall(actionConfig)
    uninstall.Timeout = 3 * time.Minute // 等待程序停止，3分钟后判断定超时
    uninstall.KeepHistory = false

    resp, err := uninstall.Run(releaseName)
    if err != nil {
        return "", fmt.Errorf("卸载失败\n%s", err)
    }

    success := fmt.Sprintf("%s 成功卸载。", resp.Release.Name)
    logger.Debug(success)
    return success, nil
}

```

### model.go

```go
package kubestore

// DeployRequest
/**
 * 部署时用到的结构体
 */
type DeployRequest struct {
    RepoURL      string `json:"RepoURL"`      // 仓库地址
    ChartName    string `json:"ChartName"`    // Chart名称
    ChartVersion string `json:"ChartVersion"` // Chart版本
    Namespace    string `json:"Namespace"`    // 命名空间
    ReleaseName  string `json:"ReleaseName"`  // 在kubernetes中的程序名
    Values       string `json:"values"`       // 存储原始的 YAML 字符串
}

// ---------------------------------------------------------------

// ChartListResponse
/**
 * 返回指定仓库中的所有Chart信息
 */
type ChartListResponse struct {
    ChartName    string // Chart名称
    ChartVersion string // Chart版本
    AppVersion   string // 应用版本
    Description  string // 描述
}

```
