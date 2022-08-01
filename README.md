# Twitter Image Crawler

一个简单的twitter图片爬虫。根据用户的 ***@用户名***，爬取其主页上的全部图片内容。

*（仅供学习交流用途，请勿传播图片、尝试 ~~[数据删除]~~ 等不适宜行为，违者自负。）*



# 安装

运行以下命令以创建适配的虚拟环境：

```
conda create -n <env_name> python=3.8
```



运行以下命令安装依赖：

```
pip install -r requirements.txt
```



# 配置

请**务必**将仓库中的 `template_settings.json` 改名为 `twitter_settings.json`，

然后依照下述如实填写 `twitter_settings.json` 文件：



- 必须自行填写的项为：

  `headers`，`proxies`，`proxy_server`，`login_info`，`username`；

  

- 可以自行修改的项为：`config`

  `interval_between_user`：每爬取不同用户之间的时间间隔（单位：秒），

  `interval_between_download`：每次下载之间的时间间隔（单位：秒），

  `interval_between_scroll`：每次自动翻滚之间的时间间隔（单位：秒）；

  *（警告：**非常**不建议将**后两项**设置得过短，过于频繁的访问存在封IP的风险。）*

  

- 不建议修改的项为：

  `scroll_limit`：最大翻滚次数限制。
  
  由于本程序实现了自动触底检测的方法，次数过大理论上不会影响运行效率，但这也意味着程序将会爬取更长时间线范围内的图片资源；次数过小则意味着程序将只爬取最近一段时间用户分享的图片。
  
  您可以根据程序的运行实况及自身的实际需求，自行考虑更改此参数。
  
  

```
{
    "headers": {
        "user-agent": "你所需使用的用户代理"
    },
    "proxies": {
        "http": "你的http代理",
        "https": "你的https代理"
    },
    “proxy_server": "你的代理服务器（一般情况下同上）",
    
    "config": {
        "interval_between_user": 60,
        "interval_between_download": 1,
        "interval_between_scroll": 1
    },
    "scroll_limit": 200,
    
    "login_info": {
    	"username": "你的推特用户名",
    	"password": "你的推特密码"
    },
    "username": [
        "用户的@用户名"，
        "不同用户名之间换行并用逗号隔开"，
        "最后一行后不加逗号"
    ]
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

   *（您所需做的一切就是填好 `username` 列表，然后轻轻敲击，等待程序执行完毕 =））*

2. 运行过程中，程序会自动在本目录下创建 `twitter_images` 目录，并在该目录下对每个用户的 ***@用户名*** 新建一个子目录，以存放该用户主页下的所有媒体图片。

3. 终端和日志文件会实时跟进程序的运行情况。用户可打开 `twitter_crawler.log` 以查看详情。