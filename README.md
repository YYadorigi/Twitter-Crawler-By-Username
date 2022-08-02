# Twitter Image Crawler

一个简单的twitter图片爬虫。根据用户的 ***@用户名***，爬取其主页上的全部图片内容。

*（仅供学习交流用途，请勿传播图片、尝试 ~~[数据删除]~~ 等不适宜行为，违者自负。）*



# 安装

运行以下命令以创建适配的虚拟环境：

```
conda create -n <env_name> python=3.8
```

</br>

运行以下命令安装依赖：

```
pip install -r requirements.txt
```



# 配置

请**务必**将仓库中的 `template_settings.json` 改名为 `twitter_settings.json`，

然后依照下述如实填写 `twitter_settings.json` 文件：

</br>

- 必须自行填写的项为：

  `headers`，`proxies`，`proxy_server`，`login_info`，`user_media_info`；

  *（注：如果您想实现对被标记为 **敏感内容** 的图片的自动爬取，请在 `login_info` 中正确填写用户名和密码的基础上，确保您的账号的 **设置** 中已设定对敏感内容的 **自动展示**。）*

  </br>

- 可以自行修改的项为：`config`

  `interval_between_user`：每爬取不同用户之间的时间间隔（单位：秒），

  `interval_between_scroll`：每次自动翻滚之间的时间间隔（单位：秒）；

  *（警告：**非常**不建议将**后一项**设置得过短，过于频繁的自动化操作存在不稳定因素。）*

  </br>

```
{
    "headers": {
        "user-agent": "你所需使用的用户代理"
    },
    "proxies": {
        "http": "你的 http 代理",
        "https": "你的 https 代理"
    },
    “proxy_server": "你的代理服务器（一般情况下同上）",
    
    "config": {
        "interval_between_user": 10,
        "interval_between_scroll": 1
    },
    
    "login_info": {
        "username": "你的推特用户名",
        "password": "你的推特密码"
    },
    "user_media_info": {
        "用户的@用户名": 待爬取的用户的 Media 栏目的推特数
                        （无需精确，取值可以溢出但不可小于0）,
        "Twitter": 2441
    }
}
```



# 文件说明

- `twitter_crawler.py`：主程序。执行该程序以运行本爬虫。
- `twitter_settings.json`：配置文件。
- `twitter_crawler.log`：运行主程序后**自动生成**的日志文件，记录日志输出。
- `twitter_images`：运行主程序后**自动生成**的目录，按照作者 ID 分目录存放图片。
- `chromedriver.exe`：Selenium 运行所需的驱动配置。*您不需要移动或是运行它。*
- `requirements.txt`：虚拟环境的依赖包。



# 使用

1. 配置好 `twitter_settings.json` 后，直接在虚拟环境下运行 `twiter_crawler.py` 即可。

   *（您所需做的一切就是上线看看，然后填好 `user_media_info` 字典，接着轻轻敲击，等待程序执行完毕 =））*

2. 运行过程中，程序会自动在本目录下创建 `twitter_images` 目录，并在该目录下对每个用户的 ***@用户名*** 新建一个子目录，以存放该用户主页下的所有媒体图片。

3. 终端和日志文件会实时跟进程序的运行情况。用户可打开 `twitter_crawler.log` 以查看详情。

