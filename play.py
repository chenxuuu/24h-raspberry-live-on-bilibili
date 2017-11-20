#coding:utf-8
import os
import sys
import time
import random
from mutagen.mp3 import MP3
import var_set
path = var_set.path
rtmp = var_set.rtmp
live_code = var_set.live_code

def convert_time(n):
    s = n%60
    m = int(n/60)
    return '00:'+"%02d"%m+':'+"%02d"%s

while True:
    try:
        files = os.listdir(path+'/downloads')
        files.sort()
        count=0
        for f in files:
            if((f.find('.mp3') != -1) and (f.find('.download') == -1)):
                audio = MP3(path+'/downloads/'+f)
                seconds=audio.info.length   #获取时长
                print('mp3 long:'+convert_time(seconds))
                if(seconds > 600):
                    print('too long,delete')
                else:
                    pic_files = os.listdir(path+'/default_pic')
                    pic_files.sort()
                    pic_ran = random.randint(0,len(pic_files)-1)
                    print('ffmpeg -re -s 1280x720 -loop 1 -r 3 -t '+str(int(seconds))+' -f image2 -i "'+path+'/default_pic/'+pic_files[pic_ran]+'" -i "'+path+'/downloads/'+f+'" -vf ass="'+path+"/downloads/"+f.replace(".mp3",'')+'.ass'+'" -pix_fmt yuv420p -crf 24 -preset ultrafast -maxrate 1000k -acodec aac -b:a 192k -c:v h264_omx -f flv "'+rtmp+live_code+'"')
                    os.system('ffmpeg -re -s 1280x720 -loop 1 -r 3 -t '+str(int(seconds))+' -f image2 -i "'+path+'/default_pic/'+pic_files[pic_ran]+'" -i "'+path+'/downloads/'+f+'" -vf ass="'+path+"/downloads/"+f.replace(".mp3",'')+'.ass'+'" -pix_fmt yuv420p -crf 24 -preset ultrafast -maxrate 1000k -acodec aac -b:a 192k -c:v h264_omx -f flv "'+rtmp+live_code+'"')
                try:
                    os.remove(path+'/downloads/'+f)
                    os.remove(path+'/downloads/'+f.replace(".mp3",'')+'.ass')
                    os.remove(path+'/downloads/'+f.replace(".mp3",'')+'.info')
                except:
                    print('delete error')
                count+=1
            if((f.find('.mp4') != -1) and (f.find('.download') == -1)):
                print('mp4:'+f)
                print('ffmpeg -re -i "'+path+"/downloads/"+f+'" -vf ass="'+path+"/downloads/"+f.replace(".mp4",'')+'.ass" -vcodec libx264 -preset ultrafast -acodec aac -b:a 192k -f flv "'+rtmp+live_code+'"')
                os.system('ffmpeg -re -i "'+path+"/downloads/"+f+'" -vf ass="'+path+"/downloads/"+f.replace(".mp4",'')+'.ass" -vcodec libx264 -preset ultrafast -acodec aac -b:a 192k -f flv "'+rtmp+live_code+'"')
                try:
                    os.remove(path+'/downloads/'+f)
                    os.remove(path+'/downloads/'+f.replace(".mp4",'')+'.ass')
                    os.remove(path+'/downloads/'+f.replace(".mp4",'')+'.info')
                except:
                    print('delete error')
                count+=1
        if(count == 0):
            print('no media')
            mp3_files = os.listdir(path+'/default_mp3')
            mp3_files.sort()
            mp3_ran = random.randint(0,len(mp3_files)-1)
            
            if(mp3_files[mp3_ran].find('.mp3') != -1):
                pic_files = os.listdir(path+'/default_pic')
                pic_files.sort()
                pic_ran = random.randint(0,len(pic_files)-1)
                audio = MP3(path+'/default_mp3/'+mp3_files[mp3_ran])
                seconds=audio.info.length   #获取时长
                print('mp3 long:'+convert_time(seconds))
                print('ffmpeg -re -s 1280x720 -loop 1 -r 3 -t '+str(int(seconds))+' -f image2 -i "'+path+'/default_pic/'+pic_files[pic_ran]+'" -i "'+path+'/default_mp3/'+mp3_files[mp3_ran]+'" -vf ass="'+path+'/default.ass" -pix_fmt yuv420p -crf 24 -preset ultrafast -maxrate 1000k -acodec aac -b:a 192k -c:v h264_omx -f flv "'+rtmp+live_code+'"')
                os.system('ffmpeg -re -s 1280x720 -loop 1 -r 3 -t '+str(int(seconds))+' -f image2 -i "'+path+'/default_pic/'+pic_files[pic_ran]+'" -i "'+path+'/default_mp3/'+mp3_files[mp3_ran]+'" -vf ass="'+path+'/default.ass" -pix_fmt yuv420p -crf 24 -preset ultrafast -maxrate 1000k -acodec aac -b:a 192k -c:v h264_omx -f flv "'+rtmp+live_code+'"')
            if(mp3_files[mp3_ran].find('.mp4') != -1):
                print('ffmpeg -re -i "'+path+"/default_mp3/"+mp3_files[mp3_ran]+'" -vf ass="'+path+'/default.ass" -vcodec libx264 -preset ultrafast -acodec aac -b:a 192k -f flv "'+rtmp+live_code+'"')
                os.system('ffmpeg -re -i "'+path+"/default_mp3/"+mp3_files[mp3_ran]+'" -vf ass="'+path+'/default.ass" -vcodec libx264 -preset ultrafast -acodec aac -b:a 192k -f flv "'+rtmp+live_code+'"')

    except:
        print('shit')

        