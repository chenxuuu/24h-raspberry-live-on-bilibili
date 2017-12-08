from util.FFmpegCommand import *
from mutagen.mp3 import MP3

class ffmpeg(object):
    def __init__(self):
        pass

    def getMusic(self, music, output, image='', ass=''):
        builder = (FFmpegCommand()
            .loop(1)
            .pixelFormat('yuv420p')
            .crf(24)
            .preset('ultrafast')
            .maxRate('3000k')
            .audioCodec('aac')
            .bitrate(type='a', rate='192k')
            .codec(type='v', codec='h264_omx')
            .format('flv')
            .output(output)
        )

        # 处理图片
        if image != '':
            # 获取音乐时长
            audio = MP3(music)
            audioTimeLength = str(int(audio.info.length))

            builder = builder.input(filename=image, fps=3, time=audioTimeLength, format="image2")

        # 处理音乐
        builder = builder.input(filename=music)
        
        # 处理字幕
        if ass != '':
            builder = builder.ass(ass)

        return builder.build()

    def getVedio(self, vedio, output, ass=''):
        builder = (FFmpegCommand()
            .vedioCodec('copy')
            .audioCodec('copy')
            .format('flv')
            .output(output)
        )

        # 处理视频
        builder = builder.input(filename=vedio)
        
        # 处理字幕
        if ass != '':
            builder = builder.ass(ass)

        return builder.build()