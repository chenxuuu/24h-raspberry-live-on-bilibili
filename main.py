from util.FFmpeg import *
from util.Config import *
from util.Danmu import *

path = '/mnt/d/temp/blive/default_mp3/'

command = ffmpeg().getMusic(music=path + 'bx.mp3', output='a.flv', image='/home/pi/soft/blive/default_pic/ab.jpg', ass='/home/pi/soft/blive/default.ass')
command = ffmpeg().getVedio(vedio=path + 'bx.mp3', output='a.flv')

danmu = Danmu()