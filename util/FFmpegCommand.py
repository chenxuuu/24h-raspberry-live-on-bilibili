import os

class FFmpegCommand(object):

    def __init__(self):
        self.config = {
            'inputCommand': ['-re'],
            'input': [],
            'ass': [],
            'outputCommand': [],
            'output': '',
            'bin': 'ffmpeg'
        }
        pass

    def input(self, filename, time=0, fps=0, format=''):
        inputCommand = []
        if fps != 0:
            inputCommand.append('-r %s' % fps)
        if time != 0:
            inputCommand.append('-t %s' % time)
        if format != '':
            inputCommand.append('-f %s' % format)
        
        inputCommand.append('-i "%s"' % filename)
        self.config['input'].append(self.buildCommand(inputCommand))
        return self

    # -pix_fmt
    def pixelFormat(self, fmt):
        self.config['outputCommand'].append('-pix_fmt %s' % fmt)
        return self

    # x264 质量
    def crf(self, num):
        self.config['outputCommand'].append('-crf %s' % num)
        return self

    # x264 编码速度
    def preset(self, speed):
        self.config['outputCommand'].append('-preset %s' % speed)
        return self

    # 最大码率
    def maxRate(self, rate):
        self.config['outputCommand'].append('-maxrate %s' % rate)
        return self

    # 最小码率
    def minRate(self, rate):
        self.config['outputCommand'].append('-minrate %s' % rate)
        return self

    # -acodec 指定音频编码
    def audioCodec(self, code):
        self.config['outputCommand'].append('-acodec %s' % code)
        return self
    
    # -vcodec 视频编码
    def vedioCodec(self, code):
        self.config['outputCommand'].append('-vcodec %s' % code)
        return self

    # 比特码率
    def bitrate(self, rate, type=''):
        if type == '':
            self.config['outputCommand'].append('-b %s' % rate)
        else:
            self.config['outputCommand'].append('-b:%s %s' % (type, rate))
            
        return self

    # 编码方式
    def codec(self, codec, type=''):
        if type == '':
            self.config['outputCommand'].append('-c %s' % codec)
        else:
            self.config['outputCommand'].append('-c:%s %s' % (type, codec))

        return self

    # -loop 循环
    def loop(self, count):
        self.config['inputCommand'].append('-loop %s' % count)
        return self

    # 字幕
    def ass(self, filename):
        self.config['ass'].append('-vf ass="%s"' % filename)
        return self

    # -f fmt 强迫采用格式fmt
    def format(self, fmt):
        self.config['outputCommand'].append('-f %s' % fmt)
        return self
    
    # 由CommandArray转换为command
    def buildCommand(self, array):
        command = ''
        for arg in array:
            command += ("%s " % arg)
            pass
        return command.strip()

    def output(self, path):
        self.config['output'] = path
        return self

    def build(self):
        # 编译所有Command
        inputCommand = self.buildCommand(self.config['inputCommand'])
        input = self.buildCommand(self.config['input'])
        ass = self.buildCommand(self.config['ass'])
        outputCommand = self.buildCommand(self.config['outputCommand'])
        output = self.config['output']
        bin = self.config['bin']

        # 拼接Command
        command = ('%s %s %s %s %s "%s"' % (bin, inputCommand, input, ass, outputCommand, output)).strip()

        return command
