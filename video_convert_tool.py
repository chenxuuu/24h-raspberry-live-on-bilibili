#coding:utf-8
#电脑上用的视频渲染工具
#用于夜间文件的预渲染工作
#请自行用pip装好相应模块
#还有个imageio.plugins.ffmpeg.download()记得运行
#文件夹请自行更改
#本工具仅用于生成ass字幕文件，渲染请去用小丸工具箱~
import os
import ass_maker

path = 'C:\\Users\\liucx\\Desktop'
#ffmpeg_path = 'C:\\Program Files (x86)\\MarukoToolbox\\tools\\ffmpeg.exe'
maxbitrate = '1800'
files = os.listdir(path+'\\downloads') #获取所有缓存文件

for i in files:
    if i.find('.flv') != -1 or i.find('.mp4') != -1:
        print('find file:'+i)
        ass_maker.make_ass(i.replace('.flv','').replace('.mp4',''),'当前是晚间专属时间哦~时间范围：晚上23点-凌晨5点\\N大家晚安哦~做个好梦~\\N当前文件名：'+i,path)
        print('ffmpeg -threads 0 -i "'+path+'/downloads/'+i+'" -aspect 16:9 -vf "scale=1280:720, ass='+path+"/downloads/"+i.replace(".mp4",'').replace(".flv",'')+'.ass'+'" -c:v libx264 -preset ultrafast -maxrate '+maxbitrate+'k -tune fastdecode -acodec aac -b:a 192k "'+path+'/downloads/'+i+'rendering.flv"')

