#coding:utf-8
import urllib
import urllib.request
import re

#获取歌曲信息，没api可用所以只能去抓网页了23333
def get_song_info(id):
    url = "https://music.163.com/song?id="+str(id)
    postdata =urllib.parse.urlencode({

    }).encode('utf-8')
    header = {
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Encoding":"utf-8",
    "Accept-Language":"zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3",
    "Cache-Control": "max-age=0",
    "Connection":"keep-alive",
    "Host":"music.163.com",
    'Referer':'http://music.163.com/',
    "Upgrade-Insecure-Requests":"1",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.102 Safari/537.36 Vivaldi/2.0.1309.42"
    }


    req = urllib.request.Request(url,postdata,header,method = 'GET')
    html = urllib.request.urlopen(req,timeout=3)
    txt = html.read().decode('utf-8')
    #print(txt)
    song_name = ""
    song_pic = ""
    txt=txt.splitlines() #按行分割开来
    for i in txt:
        matchObj = re.match( r'\"title\": \"(.*)\",', i)
        if matchObj:    #如果匹配到了东西
            song_name = matchObj.group(1).replace("\\\"","\"")
            break
    for j in txt:
        matchObj = re.match( r'\"images\": \[\"(.*)\"\],', j)
        if matchObj:    #如果匹配到了东西
            song_pic = matchObj.group(1)
            break
    print("get info:",song_name,song_pic)
    return (song_name,song_pic)

#print(get_song_info(428350227))
