#coding:utf-8
import os
import time
def make_ass(filename, info, path, ass = ''):
    ass = ass.replace('[','Dialogue: 2,0:',40)
    ass = ass.replace(']',',07:00:00.00,left_up,,0,0,0,,',40)
    ass = ass.replace('[','Dialogue: 2,0:',50)
    ass = ass.replace(']',',07:00:00.00,center_up,,0,0,0,,')
    ass = ass.replace('[','Dialogue: 2,0:')
    ass = ass.replace(']',',07:00:00.00,right_up,,0,0,0,,')
    file_content = '''[Script Info]
Title: Default ASS file
ScriptType: v4.00+
WrapStyle: 2
Collisions: Normal
PlayResX: 960
PlayResY: 720
ScaledBorderAndShadow: yes
Video Zoom Percent: 1

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,微软雅黑,20,&H00FFFFFF,&H00FFFFFF,&H28533B3B,&H500E0A00,0,0,0,0,100.0,100.0,0.0,0.0,1,3.5546875,3.0,2,10,10,5,1
Style: left_down,微软雅黑,20,&H00FFFFFF,&H00FFFFFF,&H28533B3B,&H500E0A00,0,0,0,0,100.0,100.0,0.0,0.0,1,3.5546875,3.0,1,10,10,5,1
Style: right_down,微软雅黑,20,&H00FFFFFF,&H00FFFFFF,&H28533B3B,&H500E0A00,0,0,0,0,100.0,100.0,0.0,0.0,1,3.5546875,3.0,3,10,10,5,1
Style: left_up,微软雅黑,15,&H00FFFFFF,&H00FFFFFF,&H28533B3B,&H500E0A00,0,0,0,0,100.0,100.0,0.0,0.0,1,3.5546875,3.0,7,10,10,5,1
Style: right_up,微软雅黑,20,&H00FFFFFF,&H00FFFFFF,&H28533B3B,&H500E0A00,0,0,0,0,100.0,100.0,0.0,0.0,1,3.5546875,3.0,9,10,10,5,1
Style: center_up,微软雅黑,15,&H00FFFFFF,&H00FFFFFF,&H28533B3B,&H500E0A00,0,0,0,0,100.0,100.0,0.0,0.0,1,3.5546875,3.0,8,10,10,5,1
Style: center_down,微软雅黑,20,&H00FFFFFF,&H00FFFFFF,&H28533B3B,&H500E0A00,0,0,0,0,100.0,100.0,0.0,0.0,1,3.5546875,3.0,2,10,10,5,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 2,0:00:00.00,07:00:00.00,left_down,,0,0,0,,'''+info+'''
Dialogue: 2,0:00:00.00,07:00:00.00,right_down,,0,0,0,,基于树莓派3B\\N已开源，源码见https://biu.ee/pi-live\\N'''+'点播日期：'+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+'''
Dialogue: 2,0:00:00.00,07:00:00.00,left_up,,0,0,0,,晨旭的树莓派点播台~下面是歌词哦↓
Dialogue: 2,0:00:00.00,07:00:00.00,right_up,,0,0,0,,弹幕点播方法请看直播间简介哦~
Dialogue: 2,0:00:00.00,07:00:00.00,right_up,,0,0,0,,测试点播台，功能不断完善中
'''+ass
    file = open(path+'/downloads/'+str(filename)+'.ass','w')
    file.write(file_content)
    file.close()

    
def make_info(filename, info, path):
    file_content = info
    file = open(path+'/downloads/'+str(filename)+'.info','w')
    file.write(file_content)
    file.close()
