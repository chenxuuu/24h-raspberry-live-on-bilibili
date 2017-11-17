#coding:utf-8
import urllib
import http.cookiejar
import json
import time

#需要修改的值
roomid = '16703'
#房间id（真实id，不一定是网址里的那个数）
cookie = ''
#发送弹幕用的cookie

def send_dm(s):
    global cookie
    global roomid
    url = "http://api.live.bilibili.com/msg/send"
    postdata =urllib.parse.urlencode({	
    'color':'16777215',
    'fontsize':'25',
    'mode':'1',
    'msg':s,
    'rnd':'1510756027',
    'roomid':roomid
    }).encode('utf-8')
    header = {
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding":"utf-8",
    "Accept-Language":"zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3",
    "Connection":"keep-alive",
    "Cookie":cookie,
    "Host":"api.live.bilibili.com",
    "Referer":"http://live.bilibili.com/"+roomid,
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0"
    }
    req = urllib.request.Request(url,postdata,header)
    dm_result = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
    if len(dm_result['msg']) > 0:
        print('[error]弹幕发送失败：'+s)
        print(dm_result)
    else:
        print('[log]发送弹幕：'+s)
    time.sleep(1.5)
    
def send_dm_long(s):
    n=20
    for i in range(0, len(s), n):
        send_dm(s[i:i+n])

def get_dm():
    global temp_dm
    global roomid
    url = "http://api.live.bilibili.com/ajax/msg"
    postdata =urllib.parse.urlencode({	
    'token:':'',
    'csrf_token:':'',
    'roomid':roomid
    }).encode('utf-8')
    header = {
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding":"utf-8",
    "Accept-Language":"zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3",
    "Connection":"keep-alive",
    "Host":"api.live.bilibili.com",
    "Referer":"http://live.bilibili.com/"+roomid,
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0"
    }
    req = urllib.request.Request(url,postdata,header)
    dm_result = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
    #for t_get in dm_result['data']['room']:
        #print('[log]['+t_get['timeline']+']'+t_get['nickname']+':'+t_get['text'])
    return dm_result

def check_dm(dm):
    global temp_dm
    for t_get in temp_dm['data']['room']:
        if((t_get['text'] == dm['text']) & (t_get['timeline'] == dm['timeline'])):
            return False
    return True

def get_dm_loop():
    global temp_dm
    temp_dm = get_dm()
    while True:
        dm_result = get_dm()
        can_show = False
        for t_get in dm_result['data']['room']:
            if(check_dm(t_get)):
                print('[log]['+t_get['timeline']+']'+t_get['nickname']+':'+t_get['text'])
                #send_dm('用户'+t_get['nickname']+'发送了'+t_get['text']) #别开，会死循环
        temp_dm = dm_result
        time.sleep(1)

#print('程序已启动，连接房间id：'+roomid)
#print(get_dm())
# while True:
#     try:
#         get_dm_loop()
#     except:
#         print('shit')