from util.Config import Config
import urllib
import urllib.request
import json
import time

class Danmu(object):
    def __init__(self):
        self.config = Config()
        self.httpConfig = {
            'getUrl': 'http://api.live.bilibili.com/ajax/msg',
            'sendUrl': 'http://api.live.bilibili.com/msg/send',
            'header': {
                "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Encoding":"utf-8",
                "Accept-Language":"zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3",
                "Connection":"keep-alive",
                "Cookie": self.config.get('cookie'),
                "Host":"api.live.bilibili.com",
                "Referer":"http://live.bilibili.com/" + self.config.get('roomId'),
                "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0"
            }
        }
        self.sendLock = False

    def get(self):
        # 准备数据
        roomId = self.config.get('roomId')
        postData = urllib.parse.urlencode({	'token:': '', 'csrf_token:': '', 'roomid': roomId }).encode('utf-8')

        # 发送请求
        request = urllib.request.Request(self.httpConfig['getUrl'], postData, self.httpConfig['header'])
        response = json.loads(urllib.request.urlopen(request).read().decode('utf-8'))

        # 获取最后的弹幕时间
        configTimestamp = self.config.get(module='danmu', key='timestamp')
        if configTimestamp == None:
            configTimestamp = 0
        else:
            configTimestamp = float(configTimestamp)

        if 'code' in response and response['code'] == 0:
            # 解析弹幕
            result = []
            for danmu in response['data']['room']:

                # 判断弹幕是否被处理过
                thisTimestamp = time.mktime(time.strptime(danmu['timeline'], "%Y-%m-%d %H:%M:%S"))
                if configTimestamp >= thisTimestamp:
                    continue
                
                self.config.set(module='danmu', key='timestamp', value=thisTimestamp)
                
                result.append({
                    'name': danmu['nickname'],
                    'time': danmu['timeline'],
                    'uid': str(danmu['uid']),
                    'text': danmu['text']
                })
                pass
            return result
        else:
            raise Exception('Cookie 无效')

    def send(self, text):
        elapsedTime = 0
        while self.sendLock:
            time.sleep(1)
            # 判断等待超时
            elapsedTime += 1
            if (elapsedTime > 30):
                return None
        
        # 判断长度
        lengthLimit = 20
        if len(text) > lengthLimit:
            for i in range(0, len(text), lengthLimit):
                self.send(text[i:i + lengthLimit])
                time.sleep(1.5)
            return True
        
        # 准备数据
        self.sendLock = True
        try:
            roomId = self.config.get('roomId')
            postData = (urllib.parse.urlencode({
                            'color': '16777215',
                            'fontsize': '25',
                            'mode': '1',
                            'msg': text,
                            'rnd': '1512718534',
                            'roomid': roomId
                        }).encode('utf-8'))

            # 发送请求
            request = urllib.request.Request(self.httpConfig['sendUrl'], postData, self.httpConfig['header'])
            response = json.loads(urllib.request.urlopen(request).read().decode('utf-8'))

            return 'code' in response and response['code'] == 0
        except Exception as e:
            raise e
        finally:
            self.sendLock = False
