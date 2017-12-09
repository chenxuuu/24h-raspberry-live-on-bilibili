import urllib
import urllib.request
import json
import socket

class Request(object):

    @staticmethod
    def jsonGet(url, params={}, header={}):
        if params:
            # 判断最后一位是否为?
            paramStr = urllib.parse.urlencode(params)

            if len(url) != 0 and url[len(url) - 1] != '?':
                url += '?' + paramStr
            else:
                url += url + paramStr
        
        # 发送请求
        request = urllib.request.Request(url=url, headers=header, method='GET')
        if not header:
            request = urllib.request.Request(url=url, method='GET')

        response = json.loads(urllib.request.urlopen(request).read().decode('utf-8'))
        return response
    
    @staticmethod
    def jsonPost(url, params={}, header={}):
        # 判断是否需要转换
        postStr = ''
        if isinstance(params, str):
            postStr = params
        else:
            postStr = urllib.parse.urlencode(params)

        postData = postStr.encode('utf-8')
        # 发送请求
        request = urllib.request.Request(url=url, data=postData, headers=header, method='POST')
        if not header:
            request = urllib.request.Request(url=url, data=postData, method='POST')

        response = json.loads(urllib.request.urlopen(request).read().decode('utf-8'))
        return response
    
    @staticmethod
    def download(url, savePath, callback=None):
        # 设置下载超时时间
        socket.setdefaulttimeout(600)
        urllib.request.urlretrieve(url, savePath, callback)