<h1 align="center">Twikoo_Backup</h1>
<p align="center">
      			<a style="margin-inline:5px" target="_blank" href="">
				<img  src="https://visitor-badge.glitch.me/badge?page_id=Twikoo_Backup" title="访客"/>
			</a>
</p>

# 功能

将[Twikoo](https://github.com/imaegoo/twikoo)评论数据定时备份

# 问题背景

最近我在十年之约大群中，不少群友博客被刷评论，少则几百条多则上千条，应该是用了什么脚本，且都是typecho驱动

![image](https://testingcf.jsdelivr.net/gh/GC-ZF/Twikoo_Backup/img/example.png)


# 解决办法

通过作者完善评论系统是肯定无法实现的，文件需要我们自己去备份

我第一次建站，毫无经验，所以从未考虑过备份评论，但以防万一，提供两种备份方案，写给和我一样的小白站长

宝塔可以直接对站点备份，但评论备份无法实现，服务器自带python环境，所以我做了一个python代码，利用`crontab -e`或宝塔面板中的计划任务定时备份，在目录下**backuplog.txt**会记录每一次备份日志

# Vercel部署备份方案

[下载MongoDB工具](https://www.mongodb.com/try/download/database-tools)，放到服务器里解压

![image](https://testingcf.jsdelivr.net/gh/GC-ZF/Twikoo_Backup/img/MongoDB%20tool.png)

Vercel部署，即仓库中`MongoDB.py`，将代码存放在MongoDB 数据库工具同级路径下，按需修改24行（清理备份，delete_day）、29行（Vercel部署中的MONGODB_URI去掉问号之后的东西）

```tex
# Vercel部署日志文件示例
--------------------------------------------------------------

2022年8月8日 备份失败，请检查python文件中MONGODB_URI值是否正确

--------------------------------------------------------------

2022年8月8日 备份成功
```

# 私有部署备份方案

私有部署，即仓库中`Private.py`，代码存放位置任意，修改24行（清理备份delete_day）、29行（原始路径init_path）、30行（备份路径backup_path）,都用绝对路径，但不要在相同路径下，因为定时清理会清掉所有json文件

```tex
# 私有部署日志文件示例
--------------------------------------------------------------

2022年8月8日 备份成功

--------------------------------------------------------------

2022年8月8日 备份失败，请检查python文件中init_path和backup_path是否正确或备份路径是否有读写权限
```

# 定时运行

立即导出可以在`shell`窗口中运行`python3 文件名`，定时运行方法很多，`crontab -e`、宝塔计划任务、workflow...

## 宝塔计划任务

此方法适合有服务器的人，以宝塔计划任务为例，定时Shell脚本示例，cd后跟py文件的绝对路径

```shell
cd /xxx/twikoo/mongodb/bin
python3 backup.py
```

## workflow

此方法适合无服务器的人，如果你会工作流，可以将Action中的文件作为一个私有仓库(py中有密码所以不要做公有)，将修改好的`MongoDB.py`或`Private.py`放入仓库，修改`backup.yml`中30行为你的py文件名字，修改38、39、41行(如果你不会用git，可以不改，这项意义不大)，之后该仓库会每天自动备份一次评论数据

目录结构示例
```
│  MongoDB.py
│  mongoimport.exe
│
└─.github
    └─workflows
            backup.yml
```	    
