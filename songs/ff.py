# -*- coding:utf-8 -*-
import os
import urllib
import eyed3
import time
import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

for i in range(1, 30+1):
  if(os.path.exists('/home/pi/songs/'+str(i)+'.mp3')):
    fileout = file('/usr/share/nginx/www/songs/now.js','w')
    fileout.write('t.innerHTML=("文件'+str(i)+'.mp3下载失败，任务取消")')
    fileout.close()
    os.remove('/home/pi/songs/'+str(i)+'.mp3')
    os.remove('/home/pi/songs/'+str(i)+'ok.png')
    os.remove('/usr/share/nginx/www/songs/'+str(i)+'.txt')
    os.remove('/usr/share/nginx/www/songs/'+str(i)+'.id')
  if(os.path.exists('/usr/share/nginx/www/songs/'+str(i)+'.txt')):
    f = open('/usr/share/nginx/www/songs/'+str(i)+'.txt')
    content = f.read()
    fid = open('/usr/share/nginx/www/songs/'+str(i)+'.id')
    id = fid.read()
    font = ImageFont.truetype('/home/pi/songs/qpt.ttf',30)
    imageFile = '/home/pi/songs/'+str(i)+'.png'
    im1=Image.open(imageFile)
    draw = ImageDraw.Draw(im1)
    draw.text((10, 10),unicode("本曲网易云音乐id:"+id, 'utf-8'),(0,0,255),font=font)
    draw = ImageDraw.Draw(im1)
    im1.save('/home/pi/songs/'+str(i)+'ok.png')
    fileout = file('/usr/share/nginx/www/songs/now.js','w')
    fileout.write('t.innerHTML=("正在下载'+str(i)+'.mp3")')
    fileout.close()
    urllib.urlretrieve(content, '/home/pi/songs/'+str(i)+'.mp3')
    print('download success')
    xx=eyed3.load('/home/pi/songs/'+str(i)+'.mp3')
    seconds=xx.info.time_secs
    if(seconds<600):
      fileout = file('/usr/share/nginx/www/songs/now.js','w')
      fileout.write('t.innerHTML=("正在生成'+str(i)+'.mp4的一图流视频 第一步/共两步")')
      fileout.close()
      os.system('ffmpeg -loop 1 -r 1 -t '+str(seconds)+' -f image2 -i /home/pi/songs/'+str(i)+'ok.png -vcodec libx264 -pix_fmt yuv420p -crf 24 -y /home/pi/songs/SinglePictureVideo.mp4')
      fileout = file('/usr/share/nginx/www/songs/now.js','w')
      fileout.write('t.innerHTML=("正在将'+str(i)+'.flv的视频与音频合为一体 第二步/共两步")')
      fileout.close()
      os.system('ffmpeg -i /home/pi/songs/SinglePictureVideo.mp4 -i /home/pi/songs/'+str(i)+'.mp3 -c:v copy -c:a aac -y /home/pi/songs/'+str(i)+'.flv')
      os.remove('/home/pi/songs/'+str(i)+'.mp3')
      os.remove('/home/pi/songs/SinglePictureVideo.mp4')
      os.remove('/home/pi/songs/'+str(i)+'ok.png')
      os.remove('/usr/share/nginx/www/songs/'+str(i)+'.txt')
      os.remove('/usr/share/nginx/www/songs/'+str(i)+'.id')
      fileout = file('/usr/share/nginx/www/songs/now.js','w')
      fileout.write('t.innerHTML=("成功渲染'+str(i)+'.flv！等待渲染下一个视频")')
      fileout.close()
      fileout = file('/usr/share/nginx/www/songs/'+str(i)+'.now','w')
      fileout.write(id)
      fileout.close()
    else:
      fileout = file('/usr/share/nginx/www/songs/now.js','w')
      fileout.write('t.innerHTML=("文件'+str(i)+'.mp3时长超过10分钟，任务取消")')
      fileout.close()
      os.remove('/usr/share/nginx/www/songs/'+str(i)+'.id')
      os.remove('/home/pi/songs/'+str(i)+'.mp3')
      os.remove('/usr/share/nginx/www/songs/'+str(i)+'.txt')
    #time.sleep(60)
time.sleep(10)

