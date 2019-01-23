#coding:utf-8
import os

#需要修改的值

deviceType = "pi"
#设备类型，可选类型为"pi"和"vps"，区分大小写

path = os.path.abspath('.')
#本文件的路径，请修改

roomid = '16703'
#房间id（真实id，不一定是网址里的那个数）

cookie = ''
#发送弹幕用的cookie
csrf_token = ''
#发送弹幕用的csrf_token

download_api_url = 'https://qq.papapoi.com/163music/'
#获取音乐链接的api网址，服务器性能有限，尽量请换成自己的，php文件在php文件夹

rtmp = 'rtmp://xxxxx.live-send.acg.tv/live-xxxxx/'
#直播给的两个码，填在这里
live_code = ''

free_space=15360
#允许download/default_mp3文件夹占用空间大小，超过时自动按时间顺序删除视频/音乐，单位：MiB

maxbitrate='3000'
#允许的最大码率，单位k，字符串类型，切勿改成数值型

dm_size=20
#每段弹幕的最大长度（20级以后可发30字）

use_gift_check = False
#是否使用投礼物才让点歌的设定

play_videos_when_night = False
#是否播放晚间专属视频？
