---
title: "Milvus数据库备份迁移"
date: "2023-11-16"
categories: 
  - "milvus"
---

# Milvus数据库备份迁移

> Milvus 数据库迁移，它迁移的是向量数据，并它并没有把索引也迁移过去，所以新向量库的检索会有概率性的结果不同。

## 下载工具

```bash
[root@localhost siyu.mao]# wget https://github.com/zilliztech/milvus-backup/releases/download/v0.4.2/milvus-backup_Linux_x86_64.tar.gz

[root@localhost siyu.mao]# tar -zxvf milvus-backup_Linux_x86_64.tar.gz
README.md
milvus-backup


## 添加到当前用户
[root@localhost siyu.mao]# mv milvus-backup /usr/local/bin/

## 查看
[root@localhost siyu.mao]# milvus-backup -h
0.4.2 (Built on 2023-11-08T03:28:20Z from Git SHA 84e72fc70b0492591bf7e6081c10bd89887f0bae)
milvus-backup is a backup&restore tool for milvus.

Usage:
  milvus-backup [flags]
  milvus-backup [command]

Available Commands:
  check       check if the connects is right.
  create      create subcommand create a backup.
  delete      delete subcommand delete backup by name.
  get         get subcommand get backup by name.
  help        Help about any command
  list        list subcommand shows all backup in the cluster.
  restore     restore subcommand restore a backup.
  server      server subcommand start milvus-backup RESTAPI server.

Flags:
      --config string   config YAML file of milvus (default "backup.yaml")
  -h, --help            help for milvus-backup
  -v, --version         version for milvus-backup

```

# 备份

### 为milvus-backup配置数据库相关信息[backup.yaml](https://github.com/zilliztech/milvus-backup/blob/main/configs/backup.yaml)

```yaml
# 配置系统日志输出。
log:
  level: info # 仅支持 debug、info、warn、error、panic 或 fatal。默认 'info'。
  console: true # 是否将日志打印到控制台
  file:
    rootPath: "logs/backup.log"

http:
  simpleResponse: true

# Milvus 代理地址，与 milvus.yaml 兼容
milvus:
  address: 10.200.3.101
  port: 19530
  authorizationEnabled: false
  # TLS 模式值 [0, 1, 2]
  # 0 为关闭，1 为单向认证，2 为双向认证。
  tlsMode: 0
  user: "root"
  password: "Milvus"

# 与 Milvus 相关的 MinIO 配置，负责 Milvus 的数据持久化。
minio:
  cloudProvider: "minio" # 远程云存储提供者：s3、gcp、aliyun、azure

  address: 10.200.3.101 # MinIO/S3 的地址
  port: 9000   # MinIO/S3 的端口
  accessKeyID: minioadmin  # MinIO/S3 的 accessKeyID
  secretAccessKey: minioadmin # MinIO/S3 的加密字符串
  useSSL: false # 使用 SSL 访问 MinIO/S3
  useIAM: false
  iamEndpoint: ""

  bucketName: "milvus-bucket" # MinIO/S3 中 Milvus Bucket 的名称，与您的 Milvus 实例相同
  rootPath: "file" # MinIO/S3 中 Milvus 存储的根路径，与您的 Milvus 实例相同

  # 仅适用于 Azure
  backupAccessKeyID: minioadmin  # MinIO/S3 的 accessKeyID
  backupSecretAccessKey: minioadmin # MinIO/S3 的加密字符串

  backupBucketName: "milvus-bucket" # 用于存储备份数据的 Bucket 名称。备份数据将存储在 backupBucketName/backupRootPath 中
  backupRootPath: "backup" # 存储备份数据的根路径。备份数据将存储在 backupBucketName/backupRootPath 中

backup:
  maxSegmentGroupSize: 2G
  parallelism: 2 # 用于备份的集合级并行性
  copydata:
    # 为每个集合备份复制数据的线程池，默认为 100。
    # 这意味着如果设置 backup.parallelism = 2 backup.copydata.parallelism = 100，
    # 将同时执行 200 个复制操作。
    # 如果阻塞存储的网络带宽，请减少此值。
    parallelism: 128
  keepTempFiles: false

restore:
  # 用于还原的集合级并行性
  # 仅在有多个数据节点时将其更改为 > 1。
  # 因为 Milvus bulkinsert 的最大并行性等于数据节点的数量。
  parallelism: 2

```

> 配置文件只需放在你当前命令执行时所在的目录，也可以使用`--config`来指定

### 使用命令行备份

> - `milvus-backup check`
>     
> - ```bash
>     [root@localhost siyu.mao]# milvus-backup check
>     
>     0.4.2 (Built on 2023-11-08T03:28:20Z from Git SHA 84e72fc70b0492591bf7e6081c10bd89887f0bae)
>     config:backup.yaml
>     [2023/11/15 17:11:36.800 +08:00] [INFO] [logutil/logutil.go:165] ["Log directory"] [configDir=]
>     [2023/11/15 17:11:36.800 +08:00] [INFO] [logutil/logutil.go:166] ["Set log file to "] [path=logs/backup.log]
>     [2023/11/15 17:11:36.811 +08:00] [INFO] [storage/minio_chunk_manager.go:130] ["minio chunk manager init success."] [bucketname=milvus-bucket] [root=file]
>     Succeed to connect to milvus and storage.
>     Milvus version: v2.3.1
>     Storage:
>     milvus-bucket: milvus-bucket
>     milvus-rootpath: file
>     backup-bucket: milvus-bucket
>     backup-rootpath: backup
>     
>     ```
>     
> - `milvus-backup create -n <备份名称>`
>     
> - ```bash
>     [root@localhost siyu.mao]# milvus-backup create -n milvus_backup
>     
>     0.4.2 (Built on 2023-11-08T03:28:20Z from Git SHA 84e72fc70b0492591bf7e6081c10bd89887f0bae)
>     config:backup.yaml
>     [2023/11/15 17:19:00.794 +08:00] [INFO] [logutil/logutil.go:165] ["Log directory"] [configDir=]
>     [2023/11/15 17:19:00.795 +08:00] [INFO] [logutil/logutil.go:166] ["Set log file to "] [path=logs/backup.log]
>     [2023/11/15 17:19:00.796 +08:00] [INFO] [core/backup_impl_create_backup.go:27] ["receive CreateBackupRequest"] [requestId=034172ea-8398-11ee-9811-0050560106e6] [backupName=milvus_backup] [collections="[]"] [databaseCollections=] [async=false]
>     [2023/11/15 17:19:00.796 +08:00] [INFO] [core/backup_context.go:97] ["{Base:0xc0004fcc80 MaxSegmentGroupSize:2147483648 BackupParallelism:2 RestoreParallelism:2 BackupCopyDataParallelism:128 KeepTempFiles:false}"]
>     [2023/11/15 17:19:00.796 +08:00] [INFO] [core/backup_context.go:98] ["{Base:0xc0004fcc80 Enabled:true DebugMode:false SimpleResponse:true}"]
>     [2023/11/15 17:19:00.804 +08:00] [INFO] [storage/minio_chunk_manager.go:130] ["minio chunk manager init success."] [bucketname=milvus-bucket] [root=file]
>     [2023/11/15 17:19:00.819 +08:00] [INFO] [core/backup_impl_create_backup.go:564] ["Start collection level backup pool"] [parallelism=2]
>     [2023/11/15 17:19:00.825 +08:00] [INFO] [core/backup_impl_create_backup.go:581] ["collections to backup"] [collections="[test_lock]"]
>     [2023/11/15 17:19:00.825 +08:00] [INFO] [core/backup_impl_create_backup.go:225] ["start backup collection"] [db=default] [collection=test_lock]
>     [2023/11/15 17:19:00.829 +08:00] [INFO] [core/backup_impl_create_backup.go:258] ["try to get index"] [collection_name=test_lock]
>     [2023/11/15 17:19:01.042 +08:00] [INFO] [core/backup_impl_create_backup.go:278] ["field index"] [collection_name=test_lock] [field_name=source] ["index info"="[{}]"]
>     [2023/11/15 17:19:01.050 +08:00] [INFO] [core/backup_impl_create_backup.go:278] ["field index"] [collection_name=test_lock] [field_name=text] ["index info"="[{}]"]
>     [2023/11/15 17:19:01.056 +08:00] [INFO] [core/backup_impl_create_backup.go:278] ["field index"] [collection_name=test_lock] [field_name=pk] ["index info"="[{}]"]
>     [2023/11/15 17:19:01.062 +08:00] [INFO] [core/backup_impl_create_backup.go:278] ["field index"] [collection_name=test_lock] [field_name=vector] ["index info"="[{}]"]
>     [2023/11/15 17:19:01.075 +08:00] [INFO] [core/backup_impl_create_backup.go:366] ["GetPersistentSegmentInfo before flush from milvus"] [collectionName=test_lock] [segmentNumBeforeFlush=0]
>     [2023/11/15 17:19:01.696 +08:00] [INFO] [core/backup_impl_create_backup.go:374] ["flush segments"] [collectionName=test_lock] [newSealedSegmentIDs="[445557014777791511]"] [flushedSegmentIDs="[]"] [timeOfSeal=1700039940]
>     [2023/11/15 17:19:01.700 +08:00] [INFO] [core/backup_impl_create_backup.go:387] ["GetPersistentSegmentInfo after flush from milvus"] [collectionName=test_lock] [segmentNumBeforeFlush=0] [segmentNumAfterFlush=1]
>     [2023/11/15 17:19:01.700 +08:00] [INFO] [core/backup_impl_create_backup.go:434] ["Finished fill segment"] [collectionName=test_lock]
>     [2023/11/15 17:19:01.701 +08:00] [INFO] [core/backup_impl_create_backup.go:437] ["reading SegmentInfos from storage, this may cost several minutes if data is large"] [collectionName=test_lock]
>     [2023/11/15 17:19:01.765 +08:00] [INFO] [core/backup_impl_create_backup.go:469] ["readSegmentInfo from storage"] [collectionName=test_lock] [segmentNum=1]
>     [2023/11/15 17:19:01.765 +08:00] [INFO] [core/backup_impl_create_backup.go:497] ["finish build partition info"] [collectionName=test_lock] [partitionNum=1]
>     [2023/11/15 17:19:01.765 +08:00] [INFO] [core/backup_impl_create_backup.go:501] ["Begin copy data"] [collectionName=test_lock] [segmentNum=1]
>     [2023/11/15 17:19:01.765 +08:00] [INFO] [core/backup_impl_create_backup.go:533] ["partition size is smaller than MaxSegmentGroupSize, won't separate segments into groups in backup files"] [collectionId=445557014777591483] [partitionId=445557014777591484] [partitionSize=643291] [MaxSegmentGroupSize=2147483648]
>     [2023/11/15 17:19:02.061 +08:00] [INFO] [core/backup_impl_create_backup.go:622] ["finish executeCreateBackup"] [requestId=034172ea-8398-11ee-9811-0050560106e6] [backupName=milvus_backup] [collections="[]"] [async=false] ["backup meta"="{\"id\":\"034172ea-8398-11ee-9811-0050560106e6\",\"state_code\":2,\"start_time\":1700039940819,\"end_time\":1700039941870,\"name\":\"milvus_backup\",\"backup_timestamp\":1700039940819,\"size\":643291,\"milvus_version\":\"v2.3.1\"}"]
>     success
>     duration:2 s
>     
>     ```
>     

### 使用MinIO客户端mc将文件下载到本地

#### [安装mc](https://milvus.io/docs/milvus_backup_cli.md#Back-up-data)

```bash
curl https://dl.min.io/client/mc/release/linux-amd64/mc \
     -o /usr/local/bin/mc


chmod +x /usr/local/bin/mc


mc -v

mc version RELEASE.2023-11-15T22-45-58Z (commit-id=4724c024c6de8bf2f072821ec85a19ef7e9b49d5)
Runtime: go1.21.4 linux/amd64
Copyright (c) 2015-2023 MinIO, Inc.
License GNU AGPLv3 <https://www.gnu.org/licenses/agpl-3.0.html>

```

#### 使用

> mc alias set 别名 `https://<ip:port> <username> <passwd>` mc ls 别名

```bash
## 创建minio服务的连接别名为minio_k8s
mc alias set minio_k8s http://10.200.3.101:9000 minioadmin minioadmin
Added `minio_k8s` successfully.


## 查看服务端配置
mc alias ls minio_k8s
minio_k8s
  URL       : http://10.200.3.101:9000
  AccessKey : minioadmin
  SecretKey : minioadmin
  API       : s3v4
  Path      : auto


## 查看minio_k8s服务器下的桶
mc ls minio_k8s
[2023-10-25 19:20:47 CST]     0B milvus-bucket/


## 查看桶的详细信息
mc ls minio_k8s --recursive
[2023-11-15 17:19:01 CST]   877B STANDARD milvus-bucket/backup/milvus_backup/binlogs/insert_log/445557014777591483/445557014777591484/445557014777791511/0/445640105682462922
[2023-11-15 17:19:01 CST]   487B STANDARD milvus-bucket/backup/milvus_backup/binlogs/insert_log/445557014777591483/445557014777591484/445557014777791511/1/445640105682462922
[2023-11-15 17:19:01 CST]   956B STANDARD milvus-bucket/backup/milvus_backup/binlogs/insert_log/445557014777591483/445557014777591484/445557014777791511/100/445640105682462922
[2023-11-15 17:19:01 CST]  32KiB STANDARD milvus-bucket/backup/milvus_backup/binlogs/insert_log/445557014777591483/445557014777591484/445557014777791511/101/445640105682462922
[2023-11-15 17:19:01 CST]   877B STANDARD milvus-bucket/backup/milvus_backup/binlogs/insert_log/445557014777591483/445557014777591484/445557014777791511/102/445640105682462922
[2023-11-15 17:19:01 CST] 593KiB STANDARD milvus-bucket/backup/milvus_backup/binlogs/insert_log/445557014777591483/445557014777591484/445557014777791511/103/445640105682462922
[2023-11-15 17:19:01 CST]   208B STANDARD milvus-bucket/backup/milvus_backup/meta/backup_meta.json
[2023-11-15 17:19:01 CST]   856B STANDARD milvus-bucket/backup/milvus_backup/meta/collection_meta.json
[2023-11-15 17:19:01 CST] 2.4KiB STANDARD milvus-bucket/backup/milvus_backup/meta/full_meta.json
[2023-11-15 17:19:01 CST]   146B STANDARD milvus-bucket/backup/milvus_backup/meta/partition_meta.json
[2023-11-15 17:19:01 CST] 1.1KiB STANDARD milvus-bucket/backup/milvus_backup/meta/segment_meta.json
[2023-11-15 11:24:49 CST]   877B STANDARD milvus-bucket/file/insert_log/445557014777591483/445557014777591484/445557014777791511/0/445640105682462922
[2023-11-15 11:24:49 CST]   487B STANDARD milvus-bucket/file/insert_log/445557014777591483/445557014777591484/445557014777791511/1/445640105682462922
[2023-11-15 11:24:49 CST]   956B STANDARD milvus-bucket/file/insert_log/445557014777591483/445557014777591484/445557014777791511/100/445640105682462922
[2023-11-15 11:24:49 CST]  32KiB STANDARD milvus-bucket/file/insert_log/445557014777591483/445557014777591484/445557014777791511/101/445640105682462922
[2023-11-15 11:24:49 CST]   877B STANDARD milvus-bucket/file/insert_log/445557014777591483/445557014777591484/445557014777791511/102/445640105682462922
[2023-11-15 11:24:49 CST] 593KiB STANDARD milvus-bucket/file/insert_log/445557014777591483/445557014777591484/445557014777791511/103/445640105682462922
[2023-11-15 17:19:01 CST]   503B STANDARD milvus-bucket/file/stats_log/445557014777591483/445557014777591484/445557014777791511/102/1
[2023-11-15 11:24:49 CST]   501B STANDARD milvus-bucket/file/stats_log/445557014777591483/445557014777591484/445557014777791511/102/445640105682462922
```

#### 下载备份桶

> mc cp --recursive `服务别名/<桶路径> <本地路径>`

```bash
[root@localhost siyu.mao]# mc cp --recursive minio_k8s/milvus-bucket/backup ./
..._backup/meta/segment_meta.json: 632.81 KiB / 632.81 KiB ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 6.84 MiB/s 0s


[root@localhost siyu.mao]# zip -r backup.zip backup/


[root@localhost siyu.mao]# ll -h
total 580K
drwxr-xr-x. 3 root root   27 Nov 16 10:39 backup
-rw-r--r--. 1 root root 580K Nov 16 10:41 backup.zip


```

* * *

# 恢复

### 上传到其它环境的minio上

```bash
[root@milvus (11:11:46) /data/siyu.mao/minio_backup]
└─# mc alias set minio_k8s_restore http://10.10.0.100:9000 minioadmin minioadmin
Added `minio_k8s_restore` successfully.


## 查看
[root@milvus (11:12:11) /data/siyu.mao/minio_backup]
└─# mc ls minio_k8s_restore
[2023-11-16 09:59:09 CST]     0B milvus-backup-bucket/
[2023-11-06 13:33:29 CST]     0B milvus-bucket/
[2023-11-16 10:00:41 CST]     0B mydata/


## 上传备份文件到新的minio桶中

[root@milvus (11:13:05) /data/siyu.mao/minio_backup]
└─# mc cp --recursive ./backup minio_k8s_restore/milvus-bucket/
..._backup/meta/segment_meta.json: 1.18 MiB / 1.18 MiB ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 7.28 MiB/s 0s


## 查看
[root@milvus (11:15:13) /data/siyu.mao/minio_backup]
└─# mc ls minio_k8s_restore/milvus-bucket/
[2023-11-16 11:14:59 CST] 580KiB STANDARD backup.zip
[2023-11-16 11:15:28 CST]     0B backup/
[2023-11-16 11:15:28 CST]     0B file/

```

### 将数据恢复到Milvus数据库中`backup.yaml`

```yaml
# 配置系统日志输出。
log:
  level: info # 仅支持 debug、info、warn、error、panic 或 fatal。默认 'info'。
  console: true # 是否将日志打印到控制台
  file:
    rootPath: "logs/backup.log"

http:
  simpleResponse: true

# Milvus 代理地址，与 milvus.yaml 兼容
milvus:
  address: 10.10.0.100
  port: 19530
  authorizationEnabled: false
  # TLS 模式值 [0, 1, 2]
  # 0 为关闭，1 为单向认证，2 为双向认证。
  tlsMode: 0
  user: "root"
  password: "Milvus"

# 与 Milvus 相关的 MinIO 配置，负责 Milvus 的数据持久化。
minio:
  cloudProvider: "minio" # 远程云存储提供者：s3、gcp、aliyun、azure

  address: 10.10.0.100 # MinIO/S3 的地址
  port: 9000   # MinIO/S3 的端口
  accessKeyID: minioadmin  # MinIO/S3 的 accessKeyID
  secretAccessKey: minioadmin # MinIO/S3 的加密字符串
  useSSL: false # 使用 SSL 访问 MinIO/S3
  useIAM: false
  iamEndpoint: ""

  bucketName: "milvus-bucket" # MinIO/S3 中 Milvus Bucket 的名称，与您的 Milvus 实例相同
  rootPath: "file" # MinIO/S3 中 Milvus 存储的根路径，与您的 Milvus 实例相同

  # 仅适用于 Azure
  backupAccessKeyID: minioadmin  # MinIO/S3 的 accessKeyID
  backupSecretAccessKey: minioadmin # MinIO/S3 的加密字符串

  backupBucketName: "milvus-bucket" # 用于存储备份数据的 Bucket 名称。备份数据将存储在 backupBucketName/backupRootPath 中
  backupRootPath: "backup" # 存储备份数据的根路径。备份数据将存储在 backupBucketName/backupRootPath 中

backup:
  maxSegmentGroupSize: 2G
  parallelism: 2 # 用于备份的集合级并行性
  copydata:
    # 为每个集合备份复制数据的线程池，默认为 100。
    # 这意味着如果设置 backup.parallelism = 2 backup.copydata.parallelism = 100，
    # 将同时执行 200 个复制操作。
    # 如果阻塞存储的网络带宽，请减少此值。
    parallelism: 128
  keepTempFiles: false

restore:
  # 用于还原的集合级并行性
  # 仅在有多个数据节点时将其更改为 > 1。
  # 因为 Milvus bulkinsert 的最大并行性等于数据节点的数量。
  parallelism: 2

```

### 执行恢复

> - 恢复后新集合设置后缀 xxxx`_recover`
>     - milvus-backup restore -n milvus\_backup `-s _recover`
> - 使用原集合名称，它会找到 `backupBucketName: "milvus-bucket"` 下面名为`milvus_backup`的文件夹，这个文件夹是做备份时使用`milvus-backup create -n <备份名称>`创建的
>     - milvus-backup restore -n milvus\_backup

```bash
[root@milvus (11:33:07) /data/siyu.mao/minio_backup]
└─# milvus-backup restore -n milvus_backup


0.4.2 (Built on 2023-11-08T03:28:20Z from Git SHA 84e72fc70b0492591bf7e6081c10bd89887f0bae)
[2023/11/16 11:37:26.780 +08:00] [INFO] [logutil/logutil.go:165] ["Log directory"] [configDir=]
[2023/11/16 11:37:26.780 +08:00] [INFO] [logutil/logutil.go:166] ["Set log file to "] [path=logs/backup.log]
[2023/11/16 11:37:26.780 +08:00] [INFO] [cmd/restore.go:42] ["restore cmd input args"] [args="[]"]
[2023/11/16 11:37:26.780 +08:00] [INFO] [core/backup_impl_restore_backup.go:26] ["receive RestoreBackupRequest"] [requestId=7648b8e1-8431-11ee-8450-0050560106ab] [backupName=milvus_backup] [onlyMeta=false] [restoreIndex=false] [collections="[]"] [CollectionSuffix=] [CollectionRenames={}] [async=false] [bucketName=] [path=] [databaseCollections=]
[2023/11/16 11:37:26.781 +08:00] [INFO] [core/backup_context.go:97] ["{Base:0xc000254000 MaxSegmentGroupSize:2147483648 BackupParallelism:2 RestoreParallelism:2 BackupCopyDataParallelism:128 KeepTempFiles:false}"]
[2023/11/16 11:37:26.781 +08:00] [INFO] [core/backup_context.go:98] ["{Base:0xc000254000 Enabled:true DebugMode:false SimpleResponse:true}"]
[2023/11/16 11:37:26.781 +08:00] [INFO] [core/backup_context.go:165] ["receive GetBackupRequest"] [requestId=7648cc2f-8431-11ee-8450-0050560106ab] [backupName=milvus_backup] [backupId=] [bucketName=] [path=]
[2023/11/16 11:37:26.787 +08:00] [INFO] [storage/minio_chunk_manager.go:130] ["minio chunk manager init success."] [bucketname=milvus-bucket] [root=file]
[2023/11/16 11:37:26.902 +08:00] [INFO] [core/backup_context.go:245] ["finish GetBackupRequest"] [requestId=7648cc2f-8431-11ee-8450-0050560106ab] [backupName=milvus_backup] [backupId=] [bucketName=] [path=]
[2023/11/16 11:37:26.902 +08:00] [INFO] [core/backup_impl_restore_backup.go:171] ["Collections to restore"] [collection_num=1]
[2023/11/16 11:37:26.912 +08:00] [INFO] [core/backup_impl_restore_backup.go:316] ["Start collection level restore pool"] [parallelism=2]
[2023/11/16 11:37:26.912 +08:00] [INFO] [core/backup_impl_restore_backup.go:322] ["executeRestoreBackupTask start"] [backup_name=milvus_backup] [backupBucketName=milvus-bucket] [backupPath=backup/milvus_backup]
[2023/11/16 11:37:26.912 +08:00] [INFO] [core/backup_impl_restore_backup.go:374] ["start restore"] [db_name=default] [collection_name=test_lock] [backupBucketName=milvus-bucket] [backupPath=backup/milvus_backup]
[2023/11/16 11:37:26.912 +08:00] [INFO] [core/backup_impl_restore_backup.go:401] ["collection schema"] [fields="[{\"ID\":100,\"Name\":\"source\",\"PrimaryKey\":false,\"AutoID\":false,\"Description\":\"\",\"DataType\":21,\"TypeParams\":{\"max_length\":\"65535\"},\"IndexParams\":{},\"IsDynamic\":false,\"IsPartitionKey\":false,\"ElementType\":0},{\"ID\":101,\"Name\":\"text\",\"PrimaryKey\":false,\"AutoID\":false,\"Description\":\"\",\"DataType\":21,\"TypeParams\":{\"max_length\":\"65535\"},\"IndexParams\":{},\"IsDynamic\":false,\"IsPartitionKey\":false,\"ElementType\":0},{\"ID\":102,\"Name\":\"pk\",\"PrimaryKey\":true,\"AutoID\":true,\"Description\":\"\",\"DataType\":5,\"TypeParams\":{},\"IndexParams\":{},\"IsDynamic\":false,\"IsPartitionKey\":false,\"ElementType\":0},{\"ID\":103,\"Name\":\"vector\",\"PrimaryKey\":false,\"AutoID\":false,\"Description\":\"\",\"DataType\":101,\"TypeParams\":{\"dim\":\"768\"},\"IndexParams\":{},\"IsDynamic\":false,\"IsPartitionKey\":false,\"ElementType\":0}]"]
[2023/11/16 11:37:27.124 +08:00] [INFO] [core/backup_impl_restore_backup.go:436] ["create collection"] [database=default] [collectionName=test_lock] [hasPartitionKey=false]
[2023/11/16 11:37:27.124 +08:00] [INFO] [core/backup_impl_restore_backup.go:470] ["start restore partition"] [backupCollectionName=test_lock] [targetDBName=default] [targetCollectionName=test_lock] [partition=_default]
[2023/11/16 11:37:27.128 +08:00] [INFO] [core/backup_impl_restore_backup.go:516] ["create partition"] [collectionName=test_lock] [partitionName=_default]
[2023/11/16 11:37:27.128 +08:00] [INFO] [core/backup_impl_restore_backup.go:702] [getBackupPartitionPaths] [bucketName=milvus-bucket] [backupPath=backup/milvus_backup] [partitionID=445557014777591484]
[2023/11/16 11:37:27.164 +08:00] [INFO] [core/backup_impl_restore_backup.go:670] ["bulkinsert task state"] [id=445447880708369674] [state=2] [state="{\"ID\":445447880708369674,\"State\":2,\"RowCount\":0,\"IDList\":null,\"Infos\":{\"backup\":\"true\",\"collection\":\"test_lock\",\"end_ts\":\"445655270031360\",\"failed_reason\":\"\",\"files\":\"backup/milvus_backup/binlogs/insert_log/445557014777591483/445557014777591484/,\",\"partition\":\"_default\"},\"CollectionID\":445447880708369667,\"SegmentIDs\":null,\"CreateTs\":1700105832}"] [progress=0] [currentTimestamp=1700105847] [lastUpdateTime=1700105847]
[2023/11/16 11:37:32.171 +08:00] [INFO] [core/backup_impl_restore_backup.go:670] ["bulkinsert task state"] [id=445447880708369674] [state=6] [state="{\"ID\":445447880708369674,\"State\":6,\"RowCount\":192,\"IDList\":null,\"Infos\":{\"backup\":\"true\",\"collection\":\"test_lock\",\"end_ts\":\"445655270031360\",\"failed_reason\":\"\",\"files\":\"backup/milvus_backup/binlogs/insert_log/445557014777591483/445557014777591484/,\",\"partition\":\"_default\",\"persist_cost\":\"0.48\",\"progress_percent\":\"100\"},\"CollectionID\":445447880708369667,\"SegmentIDs\":[445447880708369680],\"CreateTs\":1700105832}"] [progress=100] [currentTimestamp=1700105852] [lastUpdateTime=1700105847]
[2023/11/16 11:37:32.171 +08:00] [INFO] [core/backup_impl_restore_backup.go:485] ["finish restore partition"] [backupCollectionName=test_lock] [targetDBName=default] [targetCollectionName=test_lock] [partition=_default]
[2023/11/16 11:37:32.171 +08:00] [INFO] [core/backup_impl_restore_backup.go:345] ["finish restore collection"] [db_name=default] [collection_name=test_lock]
success
duration:6 s

```

## 验证

> 打开 attu 查看迁移结果

* * *

* * *

* * *

## 部署MinIO客户端(可选)

> 这个方案，在页面上无法打包下载 bucket ，只能一个一个的文件下载，不推荐

```bash
tee docker-compose.yaml << ERIC

version: '3.6'
services:
  minio-console:
    container_name: minio-console
    image: minio/console:v0.30.0
    ports:
      - "9090:9090"
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadmin
      CONSOLE_MINIO_SERVER: "http://10.200.3.101:9000" # 根据您的配置填写 MinIO 服务器的
    command: server /data
    volumes:
      - /etc/localtime:/etc/localtime

ERIC

```
