#coding:utf-8
import os
import sys
import time

path = 'E:\\onedrive\\wst\\24h-raspberry-live-on-bilibili'

while True:
    files = os.listdir(path+'/downloads')
    count=0
    for f in files:
        if(f.find('.mp3') != -1):
            print('mp3:'+f)
            print(f.replace(".mp3",'')+'.ass')#需改
            os.remove(path+'/downloads/'+f)
            os.remove(path+'/downloads/'+f.replace(".mp3",'')+'.ass')
            count+=1
        if(f.find('.mp4') != -1):
            print('mp4:'+f)
            print(f.replace(".mp4",'')+'.ass')#需改
            os.remove(path+'/downloads/'+f)
            os.remove(path+'/downloads/'+f.replace(".mp4",'')+'.ass')
            count+=1
    if(count == 0):
        print('no media')
        #需改