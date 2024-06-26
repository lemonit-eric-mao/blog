---
title: "Gitlab 数据备份与恢复"
date: "2019-03-06"
categories: 
  - "git"
---

##### 数据备份

**docker exec -it gitlab-ce bash `gitlab-rake gitlab:backup:create`**

```ruby
[root@gitlab gitlab-ce-13]# docker exec -it gitlab-ce bash    gitlab-rake gitlab:backup:create
2021-08-14 21:41:34 +0800 -- Dumping database ...
Dumping PostgreSQL database gitlabhq_production ... [DONE]
2021-08-14 21:41:36 +0800 -- done
2021-08-14 21:41:36 +0800 -- Dumping repositories ...
 * gitlab-instance-4431ea5d/Monitoring (@hashed/6b/86/6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b) ...
 * gitlab-instance-4431ea5d/Monitoring (@hashed/6b/86/6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b) ... [EMPTY] [SKIPPED]
 * gitlab-instance-4431ea5d/Monitoring.wiki (@hashed/6b/86/6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b.wiki) ...
 * gitlab-instance-4431ea5d/Monitoring.wiki (@hashed/6b/86/6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b.wiki) ... [EMPTY] [SKIPPED]
 * gitlab-instance-4431ea5d/Monitoring.design (@hashed/6b/86/6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b.design) ...
 * gitlab-instance-4431ea5d/Monitoring.design (@hashed/6b/86/6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b.design) ... [EMPTY] [SKIPPED]
2021-08-14 21:41:37 +0800 -- done
2021-08-14 21:41:37 +0800 -- Dumping uploads ...
2021-08-14 21:41:37 +0800 -- done
2021-08-14 21:41:37 +0800 -- Dumping builds ...
2021-08-14 21:41:37 +0800 -- done
2021-08-14 21:41:37 +0800 -- Dumping artifacts ...
2021-08-14 21:41:37 +0800 -- done
2021-08-14 21:41:37 +0800 -- Dumping pages ...
2021-08-14 21:41:37 +0800 -- done
2021-08-14 21:41:37 +0800 -- Dumping lfs objects ...
2021-08-14 21:41:37 +0800 -- done
2021-08-14 21:41:37 +0800 -- Dumping container registry images ...
2021-08-14 21:41:37 +0800 -- [DISABLED]
Creating backup archive: 1628948497_2021_08_14_13.12.10_gitlab_backup.tar ... done
Uploading backup archive to remote storage  ... skipped
Deleting tmp directories ... done
done
done
done
done
done
done
done
Deleting old backups ... skipping
Warning: Your gitlab.rb and gitlab-secrets.json files contain sensitive data
and are not included in this backup. You will need these files to restore a backup.
Please back them up manually.
Backup task is done.
[root@gitlab gitlab-ce-13]#



## 在宿主机的./data/backups/目录可是找到备份文件
[root@gitlab gitlab-ce-13]# ll ./data/backups/
total 280
-rw------- 1 zabbix polkitd 286720 Aug 14 21:41 1628948497_2021_08_14_13.12.10_gitlab_backup.tar
[root@gitlab gitlab-ce-13]#


```

* * *

* * *

* * *

##### 数据恢复

**docker exec -it gitlab-ce bash `gitlab-rake gitlab:backup:restore BACKUP=/var/opt/gitlab/backups/文件名.tar`** **特别注意：**

1. 注意文件名: 原文件名：**1628948497\_2021\_08\_14\_13.12.10\_gitlab\_backup.tar** 变化： **1628948497\_2021\_08\_14\_13.12.10\_gitlab\_backup.tar**
    
    ```ruby
    docker exec -it gitlab-ce bash    gitlab-rake gitlab:backup:restore BACKUP=/var/opt/gitlab/backups/1628948497_2021_08_14_13.12.10
    ```
    
2. 备份目录和gitlab.rb中定义的备份目录必须一致
3. gitlab的版本和备份文件中的版本必须一致，否则还原时会报错。
    
    ```ruby
    GitLab version mismatch:
    Your current GitLab version (13.12.10) differs from the GitLab version in the backup!
    Please switch to the following version and try again:
    version: 10.7.5
    ```
    

* * *

* * *

* * *
