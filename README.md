<!-- Twikoo图片 -->

<p align="center">
  <a href="https://github.com/imaegoo/twikoo"><img src="./img/logo.png" width="300" alt="twikoo"></a>
</p>
<h1 align="center">Twikoo-Comment-Backups</h1>

<!-- 徽标 -->
<p align="center">
  <a href="https://github.com/GC-ZF/Comment-Backups/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/GC-ZF/Comment-Backups" alt="license">
  </a>

  <img src="https://img.shields.io/badge/python-3.7.3+-blue" alt="python">

  <a style="margin-inline:5px" target="_blank" href="">
    <img  src="https://visitor-badge.glitch.me/badge?page_id=Comment-Backups" title="访客"/>
  </a>
</p></br>

> [Twikoo](https://github.com/imaegoo/twikoo)：一个简洁、安全、免费的静态网站评论系统

本仓库是对于Twikoo Vercel+MongoDB 部署的数据备份方案，若图片加载不出来，博文地址：[Twikoo评论定时备份方案](https://zhangshier.vip/posts/33638/)

<!-- 博客正文 -->

## 前言

Hexo博客与其它框架不同，它是前后端分离的，上个月在博客群看到了恶意刷评论的站点，这对于Hexo是致命的，解决办法就是勤备份，所以在八月初我就向作者提出了建议并附上方案[Issue #429 · imaegoo/twikoo ](https://github.com/imaegoo/twikoo/issues/429)，原本想整理发出来，但一拖再拖，方案也迭代了三次做了一些优化。最近看了[@心流的如何申请一个永久免费的 Mongodb 数据库](https://blog.panghai.top/posts/b267/)又想起来这回事了，于是优化代码、构建仓库、整理此文以及为作者附[新方案](https://github.com/imaegoo/twikoo/issues/462)

<div align="center">
  <img src="./img/Twikoo%E8%AF%84%E8%AE%BA%E5%AE%9A%E6%97%B6%E5%A4%87%E4%BB%BD%E6%96%B9%E6%A1%8801.png" alt="Twikoo评论定时备份方案01" height="500px" />
</div>

参考文档：

* [PyMongo — MongoDB Drivers](https://www.mongodb.com/docs/drivers/pymongo/)
* [PyMongo 4.2.0 documentation](https://pymongo.readthedocs.io/en/stable/tutorial.html)
* [Python操作MongoDB](https://blog.csdn.net/Java_cola/article/details/121865491)

## 特性

1. 无服务器、定时导出数据：白嫖党更多是vercel部署，所以备份方案也无需服务器嘿嘿，利用Github Actions每日定时备份，默认 `clean.cleanSecond ( 15 )` 可自定义保留天数
2. backuplog.log记录备份日志，workflows.log记录Actions运行日志（帮助小白不会使用Github而是直观的查看日志文件）
3. 使用python构建，借助 `pymongo模块` 实现数据导出。服务器自带py环境，可以直接运行导出现有数据甚至部署给服务器或本地电脑，解决评论导出/迁移的烦恼！
4. 配置简单：仅需填写仓库的`secret`，避免小白改源码发生其它错误

## 部署

在部署前，请先阅读以下三点

1. 已完成**vercel+MongoDB**部署Twikoo
2. 我们Hexo的口号是白嫖到底！此方法仅适用vercel部署的朋友，所以这种定时方案也是无服务器部署的
3. 此方案不适用私有（服务器）部署，你可以利用宝塔面板中的计划任务或`crontab -e`自定义定时任务对评论文件直接备份（宝塔可视化操作简单，不赘述）

fork项目仓库：[GC-ZF/Twikoo-Comment-Backups](https://github.com/GC-ZF/Twikoo-Comment-Backups)

![Twikoo评论定时备份方案02](./img/Twikoo%E8%AF%84%E8%AE%BA%E5%AE%9A%E6%97%B6%E5%A4%87%E4%BB%BD%E6%96%B9%E6%A1%8802.png)

进入到自己的仓库，然后点击仓库的`Settings-->Secrets-->Actions-->New repository secret`

![Twikoo评论定时备份方案03](./img/Twikoo%E8%AF%84%E8%AE%BA%E5%AE%9A%E6%97%B6%E5%A4%87%E4%BB%BD%E6%96%B9%E6%A1%8803.png)

添加环境变量secert：

| Name             | Value                                                        |
| ---------------- | ------------------------------------------------------------ |
| `GITHUBUSERNAME` | 自己的Github用户名或`github-actions[bot]`                    |
| `GITHUBEMAIL`    | 自己的Github邮箱或`github-actions[bot]@users.noreply.github.com` |
| `MONGODB_URI`    | `mongodb+srv://xxx:xxx@xxx.mongodb.net/?retryWrites=true&w=majority` |
| `DB_NAME`        | `myFirstDatabase`                                            |

- `GITHUBUSERNAME`、`GITHUBEMAIL`：是用来设置此仓库的**git配置**
- `MONGODB_URI`、`DB_NAME`：即部署Twikoo时MongoDB的数据库连接字符串，vercel与MongoDB中均可找到，以Vercel为例（第二步链接问号前没有字符串参考[MONGODB_URI和DB_NAME问题 · Issue #3](https://github.com/GC-ZF/Comment-Backups/issues/3)）
  1. 登录 [Vercel 管理后台](https://vercel.com/)，点开 `Twikoo` 的环境，点击上方的 `Settings`，点击左侧的 `Environment Variables`，在页面下方找到 `MONGODB_URI`，点击对应的小眼睛图标，会出现数据库连接地址，点击以复制这串地址
  2. 得到`mongodb+srv://xxx:xxx@xxx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority`，链接问号前的第一个字符串`myFirstDatabase`单独拿出来（不一定和我相同）

启用`fork`后仓库的`Github Actions`，点击`Actions-->I understand my workflows, go ahead and enable them`

![Twikoo评论定时备份方案04](./img/Twikoo%E8%AF%84%E8%AE%BA%E5%AE%9A%E6%97%B6%E5%A4%87%E4%BB%BD%E6%96%B9%E6%A1%8804.png)

点击`Backup twikoo-->Enable workflow`启用工作流，然后点击`Run workflow`手动运行测试

![Twikoo评论定时备份方案05](./img/Twikoo%E8%AF%84%E8%AE%BA%E5%AE%9A%E6%97%B6%E5%A4%87%E4%BB%BD%E6%96%B9%E6%A1%8805.png)

Actions运行完成后出现绿色的对勾：✅，即成功部署。若出现红色的叉：❌，根据报错尝试修改，及[Comment-Backups | issue](https://github.com/GC-ZF/Comment-Backups/issues)提问

## 导入数据

> 当评论数据发生**大量**丢失或错误无法手动修复时，可以将Github仓库中的备份数据导入。工欲善其事，必先利其器，首先选择一个好用的软件，这里推荐 **『MongoDB』**自己开发的**『MongoDBCompass』**

首先进入MongoDB网页控制台twikoo数据库下，点击Connect。（旁边Browse Collections是软件的网页版，可以进行简单的查改操作，没有导入导出等功能）

![Twikoo评论定时备份方案06](./img/Twikoo%E8%AF%84%E8%AE%BA%E5%AE%9A%E6%97%B6%E5%A4%87%E4%BB%BD%E6%96%B9%E6%A1%8806.png)

选择MongoDB Compass连接，安装软件

![Twikoo评论定时备份方案07](./img/Twikoo%E8%AF%84%E8%AE%BA%E5%AE%9A%E6%97%B6%E5%A4%87%E4%BB%BD%E6%96%B9%E6%A1%8807.png)

切记将"\<password>"替换成自己的数据库密码，再在软件中输入连接字符串

![Twikoo评论定时备份方案08](./img/Twikoo%E8%AF%84%E8%AE%BA%E5%AE%9A%E6%97%B6%E5%A4%87%E4%BB%BD%E6%96%B9%E6%A1%8808.png)

**『MongoDBCompass』** 可以帮助我们对评论增删改查，这样就拥有了类似tyepcho的评论后端，简单使用图解：

![Twikoo评论定时备份方案09](./img/Twikoo%E8%AF%84%E8%AE%BA%E5%AE%9A%E6%97%B6%E5%A4%87%E4%BB%BD%E6%96%B9%E6%A1%8809.png)

恢复评论数据方法：

1. 删除旧表：`图解蓝色方框comment三个点-->Drop Collection-->输入comment确认删除`
2. 新建表：`myFirstDatabase旁边的加号-->输入 comment 新建表-->ADD DATA导入数据`

推荐博文：[如何申请一个永久免费的 Mongodb 数据库 - 详细版 | 心流](https://blog.panghai.top/posts/b267/)，更多的连接管理方式，各有优点

类似项目：[waline评论备份 | thiscute.world](https://github.com/ryan4yin/waline-comments-backup)

## 原理

> 至此部署已全部完成，以下仅是记录一下原理，肯定有不妥之处，代码公开才会不断优化嘛

### 仓库主要目录结构

1. Comment：评论数据的Json文件

2. workflows.log：Actions 启动日志，例：

   ```tex
   备份记录 Sun Sep 25 08:49:49 CST 2022
   备份记录 Sun Sep 25 17:29:44 CST 2022
   备份记录 Mon Sep 26 08:52:16 CST 2022
   ```

3. backuplog.log：运行备份脚本的日志，例：

   ```tex
   --------------------------------------------------------------
   
   连接数据库失败，请检查变量MONGODB_URI是否正确
   
   --------------------------------------------------------------
   
   删除2022年9月10日.json
   2022年9月25日 备份成功
   
   --------------------------------------------------------------
   
   删除2022年9月11日.json
   2022年9月26日 备份成功
   ```

4. MongoDB.py：导出数据的主要代码

5. backup.yml：Actions文件，其中定时了每日UTC时间的0点自动备份一次（即北京时间8点，但可能由于Github服务器并发延迟一到两小时）

5. check.py：自用的代码，帮我筛选一些垃圾评论

Q：为什么写两个日志文件？
A：照顾部分小白不会使用Github，而是通过日志直观的查看运行情况， **workflows.log** 查看Actions是否启动，**backuplog.log** 查看备份数据是否写入 **Comment** 文件夹

**执行步骤：每日0点自启动Actions-->向workflows.log写入启动日志-->运行MongoDB.py-->导出当日数据至Comment文件夹-->向backuplog.log写入备份日志**

### 自定义备份方式

`MongoDB.py`中导出JSON有两种格式，我喜欢一行一条方便阅读，个人习惯罢了，如果需要第二种，在源码中注释方案一，解注释方案二

```python
'''
方案一，一行一条数据
例如：
    {"id":"001","name":"小张"}
    {"id":"002","name":"张张"}
'''
with open ( jsonPath, 'w', encoding="UTF-8" ) as f:
    for line in output:
        line = json.dumps ( line )
        f.writelines ( line + '\n' )
```

```python
'''
方案二，标准的JSON格式
例如：
    {
        "id":"001",
        "name":"小张"
    },
    {
        "id":"002",
        "name":"张张"
    }
'''
with open(jsonPath, 'w', encoding="UTF-8") as jf:
     jf.write(json.dumps(output, indent=1))
```

MongoDB.py中清理旧备份方案，默认方案二备份只保留近15天，方案一每月指定日期清空所有备份

```python
# clean.cleanFirst([15,30])  # 方法一，在每月15,30号清空备份
clean.cleanSecond ( 15 )  # 方法二，备份保留15天
```

> 最后强烈推荐Twikoo评论系统。作者是95后小哥，从仓库状态就可以看出，人巨好，随时回复网友的各种疑难杂症（我之前提的一个[Issues · imaegoo/twikoo](https://github.com/imaegoo/twikoo/issues/422)）。着重点名几个深得我心的功能！
>
> * 支持Valine、Disqus、Artalk、Twikoo数据迁移
> * 评论人工审核
> * 支持私有部署
> * 支持自建的[兰空图床](https://zhangshier.vip/posts/10482/)（本来是没有的，小哥专门加的）
> * 可以修改评论信息

