# blive-raspberry

`blive-raspberry`是一个为Bilibili直播编写的树莓派点歌台。

本项目重构自[晨旭的点歌台](https://github.com/chenxuuu/24h-raspberry-live-on-bilibili)。

## 使用

### 依赖安装

待补充

### 配置

本项目通过修改`config.json`来实现配置。

```json
{
    "rtmp": {
        "url": "rtmp://txy.live-send.acg.tv/live-txy/",
        "code": ""
    },
    "cookie": "",
    "roomId": 35724
}
```
- 将rtmp中的code填入你的直播码
- 在Cookie中填入你的账户的Cookie，可以使用我开发的[Bilibili Cookie获取工具](https://github.com/smilecc/blive-cookie)来获取
- 在roomId填入你的房间号

### 运行
使用Python3运行`main.py`即可
```bash
$ python3 main.py
```

## 开发

### 项目结构
```
│  config.json                  项目配置文件
│  LICENSE
│  main.py                      程序入口文件
│  README.md
│  
├─downloader                    下载器目录
│  │  NeteaseMusic.py           网易云音乐的下载器
│  │  
│  └─download                   文件下载后的存储文件夹
│          .gitignore
│          
├─log
│      .gitignore
│      ffmpeg.log               FFmpeg的日志文件
│      
├─resource                      资源文件夹
│  ├─img                        存放播放音乐时的随机图片
│  │      darksouls.jpg
│  │      
│  ├─lrc                        歌词文件夹
│  │      default.ass
│  │      
│  └─music                      无人点播时播放的随机音乐
├─service
│      Danmu.py                 弹幕服务
│      Download.py              下载服务
│      Media.py                 媒体推流服务
│      Service.py               所有Service的父类
│      
└─util                          工具
        AES.py                  AES-128-CBC加密工具
        Config.py               配置 用于读取/写入配置
        Danmu.py                弹幕 用于读取/发送弹幕
        FFmpeg.py               FFmpeg 对FFmpegCommand的封装
        FFmpegCommand.py        对FFmpeg命令行的封装
        Log.py                  日志系统
        Queue.py                队列
        Request.py              请求 用于Http请求
```

### 流程说明
```
         +---------+ 用户发送弹幕
         |
         v
+--------+---------+
|   Danmu Service  |
+--------+---------+
         | 处理并分发给下载队列
         v
+--------+---------+
| Download Service |
+--------+---------+
         | 下载完毕后通知给播放队列
         v
+--------+---------+
|   Media Service  |
+--------+---------+
         | 组织命令并推流
         v
+--------+---------+
|  Bilibili Server |
+------------------+

```
## Thanks
- [晨旭的点歌台](https://github.com/chenxuuu/24h-raspberry-live-on-bilibili)
- [FFmpeg](http://ffmpeg.org/)