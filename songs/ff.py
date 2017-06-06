# -*- coding:utf-8 -*-
import os
import urllib
import eyed3
import time
for i in range(1, 30+1):
  if(os.path.exists(str(i)+'.mp3')):
    fileout = file('/usr/share/nginx/www/songs/now.js','w')
    fileout.write('t.innerHTML=("文件'+str(i)+'.mp3下载失败，任务取消")')
    fileout.close()
    os.remove(str(i)+'.mp3')
    os.remove('/usr/share/nginx/www/songs/'+str(i)+'.txt')
  if(os.path.exists('/usr/share/nginx/www/songs/'+str(i)+'.txt')):
    f = open('/usr/share/nginx/www/songs/'+str(i)+'.txt')
    content = f.read()
    fileout = file('/usr/share/nginx/www/songs/now.js','w')
    fileout.write('t.innerHTML=("正在下载'+str(i)+'.mp3")')
    fileout.close()
    urllib.urlretrieve(content, str(i)+'.mp3')
    print('download success')
    xx=eyed3.load(str(i)+'.mp3')
    seconds=xx.info.time_secs
    if(seconds<600):
      fileout = file('/usr/share/nginx/www/songs/now.js','w')
      fileout.write('t.innerHTML=("正在生成'+str(i)+'.mp4的一图流视频 第一步/共两步")')
      fileout.close()
      os.system('ffmpeg -loop 1 -r 1 -t '+str(seconds)+' -f image2 -i '+str(i)+'.png -vcodec libx264 -pix_fmt yuv420p -crf 24 -y SinglePictureVideo.mp4')
      fileout = file('/usr/share/nginx/www/songs/now.js','w')
      fileout.write('t.innerHTML=("正在将'+str(i)+'.flv的视频与音频合为一体 第二步/共两步")')
      fileout.close()
      os.system('ffmpeg -i SinglePictureVideo.mp4 -i '+str(i)+'.mp3 -c:v copy -c:a aac -y '+str(i)+'.flv')
      os.remove(str(i)+'.mp3')
      os.remove('SinglePictureVideo.mp4')
      os.remove('/usr/share/nginx/www/songs/'+str(i)+'.txt')
      fileout = file('/usr/share/nginx/www/songs/now.js','w')
      fileout.write('t.innerHTML=("成功渲染'+str(i)+'.flv！60秒后会开始渲染下一个视频")')
      fileout.close()
    else:
      fileout = file('/usr/share/nginx/www/songs/now.js','w')
      fileout.write('t.innerHTML=("文件'+str(i)+'.mp3时长超过10分钟，任务取消")')
      fileout.close()
      os.remove(str(i)+'.mp3')
      os.remove('/usr/share/nginx/www/songs/'+str(i)+'.txt')
    time.sleep(60)
time.sleep(10)

