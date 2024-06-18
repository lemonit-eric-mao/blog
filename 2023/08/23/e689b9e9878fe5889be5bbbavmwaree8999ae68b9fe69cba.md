---
title: 批量创建VMware虚拟机
date: '2023-08-23T10:48:52+00:00'
status: private
permalink: /2023/08/23/%e6%89%b9%e9%87%8f%e5%88%9b%e5%bb%bavmware%e8%99%9a%e6%8b%9f%e6%9c%ba
author: 毛巳煜
excerpt: ''
type: post
id: 10226
category:
    - VMware
tag: []
post_format: []
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
hestia_layout_select:
    - sidebar-right
---
批量创建VMware虚拟机
=============

> 基于PowerShell + PowerCLI 13.1.0 实现批量创建VMware虚拟机

### CreateVMS.ps1

```powershell
$vc = "172.16.14.154"
$user = "account"
$password = "passwd"

# 链接vCenter
Connect-VIServer -Server $vc -Username $user -Password $password
# Disconnect-VIServer -Server $vc

# 获取脚本执行时所在的绝对路径
$scriptDirectory = Split-Path -Parent $MyInvocation.MyCommand.Path
# 切换工作目录
Set-Location -Path $scriptDirectory

# 获取虚拟机配置文件
$vmFile = ".\vms.csv"
$vms = Import-Csv $vmFile
$vmsCount = $vms.Count

Write-Host "Total number of VMs to create: $vmsCount"

# 控制台输出测试日志
function Debug-Log {
    param($vm)

    # 测试-控制台打印数据
    Write-Host @"
Creating VM with
    Portgroup: $($vm.Vlan)
    Template: $($vm.Template)
    Datastore: $($vm.Datastore)
    Name: $($vm.Name)
    ComputerName: $($vm.ComputerName)
    NumCPU: $($vm.NumCPU)
    MemoryGB: $($vm.MemoryGB)
    Rule: $($vm.Rule)
    IP: $($vm.IP)
    NetMask: $($vm.NetMask)
    Gateway: $($vm.Gateway)
-----------------------------
"@
}


# 全局参数配置，应用于虚拟机创建的必要参数
$dnsAddresses = "172.16.8.3","172.16.8.13"

$resourcePool = Get-Cluster        -Name VM_CLOUD_02
$location     = "VRM"

# 批量创建虚拟机
foreach ($vm in $vms) {
    # 输出配置文件信息，可选
    #Debug-Log -vm $vm
    # 获取CSV中配置文件中数据
    $portgroup      = Get-VDPortgroup -Name $vm.Vlan
    $template       = Get-Template    -Name $vm.Template
    $datastore      = Get-Datastore   -Name $vm.Datastore
    $name           = $vm.Name
    $computerName   = $vm.ComputerName
    $numCPU         = $vm.NumCPU
    $coresPerSocket = $vm.NumCPU
    $memoryGB       = $vm.MemoryGB
    $rule           = $vm.Rule
    $ipAddress      = $vm.IP
    $subnetMask     = $vm.NetMask
    $defaultGateway = $vm.Gateway

    # 如果CSV中提供了计算机名称，则进行设置
    if ($computerName.Length -gt 0) {
        Get-OSCustomizationSpec $rule | Set-OSCustomizationSpec -NamingScheme fixed -NamingPrefix $computerName
    }

    # 自定义虚拟机参数
    Get-OSCustomizationSpec $rule | Get-OSCustomizationNicMapping | Set-OSCustomizationNicMapping -IpMode 'UseStaticIP' -IpAddress $ipAddress -SubnetMask $subnetMask -DefaultGateway $defaultGateway
    $osCustomizationSpec = Get-OSCustomizationSpec $rule

    # 新建虚机，应用模板和自定义规范进行配置
    $vm = New-VM -Name $name -ResourcePool $resourcePool -Template $template -Datastore $datastore -Location $location -OSCustomizationSpec $osCustomizationSpec
    # 设置内存参数
    $vm | Set-VM -NumCpu $numCPU -CoresPerSocket $coresPerSocket -MemoryGB $memoryGB -Confirm:$false
    # 添加端口组
    $networkAdapter = Get-NetworkAdapter -VM $vm
    $networkAdapter | Set-NetworkAdapter -NetworkName $portgroup -Confirm:$false

    # 启动虚拟机
    Start-VM -VM $name -RunAsync
}


```

- - - - - -

### vms.csv

<table><thead><tr><th>Name</th><th>ComputerName</th><th>IP</th><th>NetMask</th><th>Gateway</th><th>NumCPU</th><th>MemoryGB</th><th>Vlan</th><th>Datastore</th><th>Template</th><th>Rule</th></tr></thead><tbody><tr><td>Test-001</td><td>bip-installer</td><td>10.16.35.31</td><td>255.255.255.0</td><td>10.16.35.30</td><td>8</td><td>32</td><td>NSX-Seg-vlan11</td><td>Datastore\_data-vol20</td><td>Template-CentOS\_7.6\_Server\_x86\_64</td><td>Rule\_Linux</td></tr><tr><td>Test-002</td><td>bip-installer</td><td>10.16.35.32</td><td>255.255.255.0</td><td>10.16.35.30</td><td>16</td><td>32</td><td>NSX-Seg-vlan11</td><td>Datastore\_data-vol20</td><td>Template-CentOS\_7.6\_Server\_x86\_64</td><td>Rule\_Linux</td></tr></tbody></table>