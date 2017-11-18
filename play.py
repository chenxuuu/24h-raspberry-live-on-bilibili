#coding:utf-8
import os
import sys
import time
from mutagen.mp3 import MP3
path = 'E:\\onedrive\\wst\\24h-raspberry-live-on-bilibili'

def convert_time(n):
    s = n%60
    m = int(n/60)
    return '00:'+"%02d"%m+':'+"%02d"%s

while True:
    files = os.listdir(path+'/downloads')
    count=0
    for f in files:
        if(f.find('.mp3') != -1):
            audio = MP3(path+'/downloads/'+f)
            seconds=audio.info.length   #获取时长
            print('mp3 long:'+convert_time(seconds))
            if(seconds > 600):
                print('too long,delete')
            else:
                print('do something') #ffmpeg -i input.mp4 -ss **START_TIME** -t **STOP_TIME** -s 1280x720 -acodec copy -vcodec copy output.mp4
            print('mp3:'+f)
            print(f.replace(".mp3",'')+'.ass')#需改
            try:
                os.remove(path+'/downloads/'+f)
                os.remove(path+'/downloads/'+f.replace(".mp3",'')+'.ass')
            except:
                print('delete error')
            count+=1
        if(f.find('.mp4') != -1):
            print('mp4:'+f)
            print(f.replace(".mp4",'')+'.ass')#需改
            try:
                os.remove(path+'/downloads/'+f)
                os.remove(path+'/downloads/'+f.replace(".mp4",'')+'.ass')
            except:
                print('delete error')
            count+=1
    if(count == 0):
        print('no media')
        exit()
        #需改