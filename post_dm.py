#coding:utf-8
import urllib
import urllib.request
import http.cookiejar
import json
import time
import os
import sys
import datetime
import time
import ass_maker
import var_set
import _thread
import random

path = var_set.path
roomid = var_set.roomid
cookie = var_set.cookie
download_api_url = var_set.download_api_url

dm_lock = False
encode_lock = False

def check_free():
    files = os.listdir(path+'/downloads')
    size = 0
    for f in files:
        size += os.path.getsize(path+'/downloads/'+f)
    files = os.listdir(path+'/default_mp3')
    for f in files:
        size += os.path.getsize(path+'/default_mp3/'+f)
    if(size > var_set.free_space*1024*1024):
        return True
    else:
        return False

def del_file(f):
    try:
        os.remove(path+'/downloads/'+f)
    except:
        print('delete error')

def get_download_url(s, t, user, song = "nothing"):
    global encode_lock
    if(check_free()):
        send_dm_long('树莓存储空间已爆炸，请联系up')
        return
    send_dm_long('正在下载'+t+str(s))
    print('[log]getting url:'+t+str(s))
    params = urllib.parse.urlencode({t: s})
    f = urllib.request.urlopen(download_api_url + "?%s" % params)
    url = f.read().decode('utf-8')
    try:
        filename = str(time.mktime(datetime.datetime.now().timetuple()))
        if(t == 'id'):
            urllib.request.urlretrieve(url, path+'/downloads/'+filename+'.mp3')
            lyric_get = urllib.parse.urlencode({'lyric': s})
            lyric_w = urllib.request.urlopen(download_api_url + "?%s" % lyric_get)
            lyric = lyric_w.read().decode('utf-8')
            if(song == "nothing"):
                ass_maker.make_ass(filename,'当前歌曲网易云id：'+str(s)+"\\N点播人："+user,path,lyric)
                ass_maker.make_info(filename,'id：'+str(s)+",点播人："+user,path)
            else:
                ass_maker.make_ass(filename,'当前网易云id：'+str(s)+"\\N点播关键词："+song+"\\N点播人："+user,path,lyric)
                ass_maker.make_info(filename,'id：'+str(s)+",点的："+song+",点播人："+user,path)
            send_dm_long(t+str(s)+'下载完成，已加入播放队列')
            print('[log]已添加排队项目：'+t+str(s))
        elif(t == 'mv'):
            urllib.request.urlretrieve(url, path+'/downloads/'+filename+'.mp4')
            if(song == "nothing"):
                ass_maker.make_ass(filename+'ok','当前MV网易云id：'+str(s)+"\\N点播人："+user,path)
                ass_maker.make_info(filename+'ok','MVid：'+str(s)+",点播人："+user,path)
            else:
                ass_maker.make_ass(filename+'ok','当前MV网易云id：'+str(s)+"\\NMV点播关键词："+song+"\\N点播人："+user,path)
                ass_maker.make_info(filename+'ok','MVid：'+str(s)+",MV："+song+",点播人："+user,path)
            send_dm_long(t+str(s)+'下载完成，等待渲染，请耐心等待')
            while (encode_lock):
                time.sleep(1)
            encode_lock = True
            send_dm_long(t+str(s)+'正在渲染，请耐心等待')
            os.system('ffmpeg -re -i "'+path+'/downloads/'+filename+'.mp4" -s 1280x720 -vf ass="'+path+"/downloads/"+filename+'ok.ass'+'" -c:v libx264 -preset ultrafast -tune fastdecode -acodec aac -b:a 192k "'+path+'/downloads/'+filename+'rendering.flv"')
            encode_lock = False
            del_file(filename+'.mp4')
            os.rename(path+'/downloads/'+filename+'rendering.flv',path+'/downloads/'+filename+'ok.flv')
            send_dm_long(t+str(s)+'渲染完毕，已加入播放队列')
        try:
            log_file = open(path+'/songs.log', 'a')
            log_file.writelines(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + ','+user+','+t+str(s)+'\r\n')
            log_file.close()
        except:
            print('[error]log error')
    except:
        send_dm('出错了：下载出错，请换一首或重试')
        print('[log]下载文件出错：'+t+str(s)+',url:'+url)
        del_file(filename+'.mp3')
        del_file(filename+'.mp4')
        del_file(filename+'.flv')
    return url

def download_bilibili(video_url,user):
    global encode_lock
    if(check_free()):
        send_dm_long('树莓存储空间已爆炸，请联系up')
        return
    try:
        print('[log]downloading bilibili video:'+str(video_url))
        video_info = json.loads(os.popen('you-get '+video_url+' --json').read())
        video_title = video_info['title']
        send_dm_long('正在下载'+video_title)
        send_dm('注意，视频下载十分费时，请耐心等待')
        filename = str(time.mktime(datetime.datetime.now().timetuple()))
        os.system('you-get '+video_url+' --format=flv -o '+path+'/downloads -O '+filename+'rendering1')
        ass_maker.make_ass(filename+'ok','番剧：'+video_title+"\\N点播人："+user,path)
        ass_maker.make_info(filename+'ok','番剧：'+video_title+",点播人："+user,path)
        send_dm_long('番剧'+video_title+'下载完成，等待渲染，请耐心等待')
        while (encode_lock):
            time.sleep(1)
        encode_lock = True
        send_dm_long('番剧'+video_title+'正在渲染，请耐心等待')
        os.system('ffmpeg -re -i "'+path+'/downloads/'+filename+'rendering1.flv" -s 1280x720 -vf ass="'+path+"/downloads/"+filename+'ok.ass'+'" -c:v libx264 -preset ultrafast -tune fastdecode -acodec aac -b:a 192k "'+path+'/downloads/'+filename+'rendering.flv"')
        encode_lock = False
        del_file(filename+'rendering1.flv')
        os.rename(path+'/downloads/'+filename+'rendering.flv',path+'/downloads/'+filename+'ok.flv')
        send_dm_long('番剧'+video_title+'渲染完毕，已加入播放队列')
    except:
        send_dm('出错了：可能下载时炸了')
        
def download_av(video_url,user):
    global encode_lock
    if(check_free()):
        send_dm_long('树莓存储空间已爆炸，请联系up')
        return
    try:
        print('[log]downloading bilibili video:'+str(video_url))
        video_info = json.loads(os.popen('you-get '+video_url+' --json').read())
        video_title = video_info['title']
        send_dm_long('正在下载'+video_title)
        send_dm('注意，视频下载十分费时，请耐心等待')
        filename = str(time.mktime(datetime.datetime.now().timetuple()))
        os.system('you-get '+video_url+' --format=flv -o '+path+'/downloads -O '+filename+'rendering1')
        print('you-get '+video_url+' --format=flv -o '+path+'/downloads -O '+filename+'rendering1')
        ass_maker.make_ass(filename+'ok','视频：'+video_title+"\\N"+video_url+"\\N点播人："+user,path)
        ass_maker.make_info(filename+'ok','视频：'+video_title+",点播人："+user,path)
        send_dm_long('视频'+video_title+'下载完成，等待渲染，请耐心等待')
        while (encode_lock):
            time.sleep(1)
        encode_lock = True
        send_dm_long('视频'+video_title+'正在渲染，请耐心等待')
        os.system('ffmpeg -re -i "'+path+'/downloads/'+filename+'rendering1.flv" -s 1280x720 -vf ass="'+path+"/downloads/"+filename+'ok.ass'+'" -c:v libx264 -preset ultrafast -tune fastdecode -acodec aac -b:a 192k "'+path+'/downloads/'+filename+'rendering.flv"')
        encode_lock = False
        del_file(filename+'rendering1.flv')
        os.rename(path+'/downloads/'+filename+'rendering.flv',path+'/downloads/'+filename+'ok.flv')
        send_dm_long('视频'+video_title+'渲染完毕，已加入播放队列')
    except:
        send_dm('出错了：可能下载时炸了')

def search_song(s,user):
    print('[log]searching song:'+s)
    params = urllib.parse.urlencode({'type': 1, 's': s})
    f = urllib.request.urlopen("http://s.music.163.com/search/get/?%s" % params)
    search_result = json.loads(f.read().decode('utf-8'))
    result_id = search_result["result"]["songs"][0]["id"]
    _thread.start_new_thread(get_download_url, (result_id, 'id', user,s))


def search_mv(s,user):
    url = "http://music.163.com/api/search/get/"
    postdata =urllib.parse.urlencode({	
    's':s,
    'offset':'1',
    'limit':'10',
    'type':'1004'
    }).encode('utf-8')
    header = {
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding":"utf-8",
    "Accept-Language":"zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3",
    "Connection":"keep-alive",
    "Host":"music.163.com",
    "Referer":"http://music.163.com/",
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0"
    }
    req = urllib.request.Request(url,postdata,header)
    result = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
    result_id = result['result']['mvs'][0]['id']
    _thread.start_new_thread(get_download_url, (result_id, 'mv', user,s))


jump_to_next_counter = 0

def pick_msg(s, user):
    global jump_to_next_counter
    global encode_lock
    if(user == '接待喵'):  #防止自循环
        return
    if(s.find('mvid+') == 0):
        send_dm('已收到'+user+'的指令')
        _thread.start_new_thread(get_download_url, (s.replace('mvid+', '', 1), 'mv',user))
    elif (s.find('mv+') == 0):
        try:
            send_dm('已收到'+user+'的指令')
            search_mv(s.replace('mv+', '', 1),user)
        except:
            print('[log]mv not found')
            send_dm('出错了：没这mv')
    elif (s.find('song+') == 0):
        try:
            send_dm('已收到'+user+'的指令')
            search_song(s.replace('song+', '', 1),user)
        except:
            print('[log]song not found')
            send_dm('出错了：没这首歌')
    elif (s.find('id+') == 0):
        send_dm('已收到'+user+'的指令')
        _thread.start_new_thread(get_download_url, (s.replace('id+', '', 1), 'id',user))
    elif(s.find('mvid') == 0):
        send_dm('已收到'+user+'的指令')
        _thread.start_new_thread(get_download_url, (s.replace('mvid', '', 1), 'mv',user))
    elif (s.find('mv') == 0):
        try:
            send_dm('已收到'+user+'的指令')
            search_mv(s.replace('mv', '', 1),user)
        except:
            print('[log]mv not found')
            send_dm('出错了：没这mv')
    elif (s.find('song') == 0):
        try:
            send_dm('已收到'+user+'的指令')
            search_song(s.replace('song', '', 1),user)
        except:
            print('[log]song not found')
            send_dm('出错了：没这首歌')
    elif (s.find('id') == 0):
        send_dm('已收到'+user+'的指令')
        _thread.start_new_thread(get_download_url, (s.replace('id', '', 1), 'id',user))
    elif (s.find('点歌') == 0):
        try:
            send_dm('已收到'+user+'的指令')
            search_song(s.replace('点歌', '', 1),user)
        except:
            print('[log]song not found')
            send_dm('出错了：没这首歌')
    elif (s.find('喵') > -1):
        replay = ["喵？？", "喵喵！", "喵。。喵？", "喵喵喵~", "喵！"]
        send_dm(replay[random.randint(0, len(replay))])  #用于测试是否崩掉
    elif (s == '切歌'):
        if(encode_lock):
            send_dm('有渲染任务，无法切歌')
            return
        jump_to_next_counter += 1
        if(jump_to_next_counter < 5):
            send_dm('已收到'+str(jump_to_next_counter)+'次切歌请求，达到五次将切歌')
        else:
            jump_to_next_counter = 0
            send_dm('已执行切歌动作')
            os.system('killall ffmpeg')
    elif ((s == '点播列表') or (s == '歌曲列表')):
        send_dm_long('已收到'+user+'的指令，正在查询')
        files = os.listdir(path+'/downloads')
        files.sort()
        songs_count = 0
        all_the_text = ""
        for f in files:
            if((f.find('.mp3') != -1) and (f.find('.download') == -1)):
                try:
                    info_file = open(path+'/downloads/'+f.replace(".mp3",'')+'.info', 'r')
                    all_the_text = info_file.read()
                    info_file.close()
                except Exception as e:
                    print(e)
                send_dm_long(all_the_text)
                songs_count += 1
            if((f.find('ok.flv') != -1) and (f.find('.download') == -1) and (f.find('rendering') == -1)):
                try:
                    info_file = open(path+'/downloads/'+f.replace(".flv",'')+'.info', 'r')
                    all_the_text = info_file.read()
                    info_file.close()
                except Exception as e:
                    print(e)
                send_dm_long(all_the_text)
                songs_count += 1
        send_dm('点播列表展示完毕，一共'+str(songs_count)+'首')
    elif (s == '渲染列表'):
        send_dm_long('已收到'+user+'的指令，正在查询')
        files = os.listdir(path+'/downloads')
        files.sort()
        songs_count = 0
        all_the_text = ""
        for f in files:
            if(f.find('rendering1.flv') != -1):
                try:
                    info_file = open(path+'/downloads/'+f.replace("rendering1.flv",'')+'ok.info', 'r')
                    all_the_text = info_file.read()
                    info_file.close()
                except Exception as e:
                    print(e)
                send_dm_long(all_the_text)
                songs_count += 1
            if(f.find('.mp4') != -1):
                try:
                    info_file = open(path+'/downloads/'+f.replace(".mp4",'')+'ok.info', 'r')
                    all_the_text = info_file.read()
                    info_file.close()
                except Exception as e:
                    print(e)
                send_dm_long(all_the_text)
                songs_count += 1
        send_dm('渲染列表展示完毕，一共'+str(songs_count)+'首')
    elif (s.find('番剧') == 0):
        try:
            send_dm('已收到'+user+'的指令')
            #番剧aaa/bbb
            ture_url=s.replace('.','/play#')
            ture_url=ture_url.replace('番剧','https://bangumi.bilibili.com/anime/')
            _thread.start_new_thread(download_bilibili, (ture_url,user))
        except:
            print('[log]video not found')
    elif (s.find('av') == 0):
        try:
            if(s.find('p') == -1):
                send_dm('已收到'+user+'的指令')
                #avxxxxx
                ture_url=s.replace('av','https://www.bilibili.com/video/av')
                _thread.start_new_thread(download_av, (ture_url,user))
            else:
                send_dm('已收到'+user+'的指令')
                #avxxxx/#page=x
                ture_url=s.replace('p','/#page=')
                ture_url=ture_url.replace('av','https://www.bilibili.com/video/av')
                _thread.start_new_thread(download_av, (ture_url,user))
        except:
            print('[log]video not found')
    elif (s.find('温度') > -1):
        send_dm_long("CPU "+os.popen('vcgencmd measure_temp').readline())
    # else:
    #     print('not match anything')






def send_dm(s):
    global cookie
    global roomid
    global dm_lock
    while (dm_lock):
        #print('[log]wait for send dm')
        time.sleep(1)
    dm_lock = True
    try:
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
    except:
        print('[error]send dm error')
    time.sleep(1.5)
    dm_lock = False
    
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
                pick_msg(t_get['text'],t_get['nickname'])
        temp_dm = dm_result
        time.sleep(1)

def test():
    print('ok')

print('程序已启动，连接房间id：'+roomid)
send_dm('弹幕监控已启动，可以点歌了')
while True:
    try:
        get_dm_loop()
    except Exception as e:
        print('shit')
        print(e)
        dm_lock = False
