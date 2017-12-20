#coding:utf-8

#需要修改的值

path = '/home/pi/live'
#本文件的路径，请修改

roomid = '16703'
#房间id（真实id，不一定是网址里的那个数）

cookie = ''
#发送弹幕用的cookie

download_api_url = 'http://qq.papapoi.com/163/'
#获取音乐链接的api网址，服务器性能有限，尽量请换成自己的，php文件在php文件夹

rtmp = 'rtmp://txy.live-send.acg.tv/live-txy/'
#直播给的两个码，填在这里
live_code = ''


free_space=15360

#允许download/default_mp3文件夹占用空间大小，超过时自动按时间顺序删除视频/音乐，单位：MiB


maxbitrate='3000'
#允许的最大码率，单位k，字符串类型，切勿改成数值型


dm_size=20
#每段弹幕的最大长度（20级以后可发30字）

