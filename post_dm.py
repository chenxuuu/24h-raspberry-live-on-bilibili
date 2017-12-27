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
import dht11

path = var_set.path         #引入设置路径
roomid = var_set.roomid     #引入设置房间号
cookie = var_set.cookie     #引入设置cookie
download_api_url = var_set.download_api_url #引入设置的音乐下载链接获取接口

dm_lock = False         #弹幕发送锁，用来排队
encode_lock = False     #视频渲染锁，用来排队

sensitive_word = ('64', '89') #容易误伤的和谐词汇表，待补充

#检查已使用空间是否超过设置大小
def check_free():
    files = os.listdir(path+'/downloads')  #获取下载文件夹下所有文件
    size = 0
    for f in files:          #遍历所有文件
        size += os.path.getsize(path+'/downloads/'+f)  #累加大小
    files = os.listdir(path+'/default_mp3')#获取缓存文件夹下所有文件
    for f in files:         #遍历所有文件
        size += os.path.getsize(path+'/default_mp3/'+f)#累加大小
    if(size > var_set.free_space*1024*1024):  #判断是否超过设定大小
        print("space size:"+str(size))
        return True
    else:
        return False

#检查已使用空间，并在超过时，自动删除缓存的视频
def clean_files():
    is_boom = True  #用来判断可用空间是否爆炸
    if(check_free()):  #检查已用空间是否超过设置大小
        files = os.listdir(path+'/default_mp3') #获取下载文件夹下所有文件
        files.sort()    #排序文件，以便按日期删除多余文件
        for f in files:
            if((f.find('.flv') != -1) & (check_free())):    #检查可用空间是否依旧超过设置大小，flv文件
                try:
                    os.remove(path+'/default_mp3/'+f)   #删除文件
                except Exception as e:
                    print(e)
            elif((f.find('.mp3') != -1) & (check_free())):    #检查可用空间是否依旧超过设置大小，mp3文件
                try:
                    os.remove(path+'/default_mp3/'+f)   #删除文件
                    os.remove(path+'/default_mp3/'+f.replace(".mp3",'')+'.ass')
                    os.remove(path+'/default_mp3/'+f.replace(".mp3",'')+'.info')
                except Exception as e:
                    print(e)
            elif(check_free() == False):    #符合空间大小占用设置时，停止删除操作
                is_boom = False
    else:
        is_boom = False
    return is_boom

#用于删除文件，防止报错
def del_file(f):
    try:
        os.remove(path+'/downloads/'+f)
    except:
        print('delete error')

#下载歌曲，传入参数：
#s：数值型，传入歌曲/mv的id
#t：type，类型，mv或id
#user：字符串型，点播者
#song：歌名，点播时用的关键字，可选
def get_download_url(s, t, user, song = "nothing"):
    global encode_lock  #视频渲染锁，用来排队
    if(clean_files()):  #检查空间是否在设定值以内，并自动删除多余视频缓存
        send_dm_long('树莓存储空间已爆炸，请联系up')
        return
    send_dm_long('正在下载'+t+str(s))
    print('[log]getting url:'+t+str(s))
    params = urllib.parse.urlencode({t: s}) #格式化参数
    f = urllib.request.urlopen(download_api_url + "?%s" % params)   #设定获取的网址
    url = f.read().decode('utf-8')  #读取结果
    try:
        filename = str(time.mktime(datetime.datetime.now().timetuple()))    #获取时间戳，用来当作文件名
        if(t == 'id'):  #当参数为歌曲时
            urllib.request.urlretrieve(url, path+'/downloads/'+filename+'.mp3') #下载歌曲
            lyric_get = urllib.parse.urlencode({'lyric': s})    #格式化参数
            lyric_w = urllib.request.urlopen(download_api_url + "?%s" % lyric_get)  #设定获取歌词的网址
            lyric = lyric_w.read().decode('utf-8')  #获取歌词文件

            tlyric_get = urllib.parse.urlencode({'tlyric': s})    #格式化参数
            tlyric_w = urllib.request.urlopen(download_api_url + "?%s" % tlyric_get)  #设定获取歌词的网址
            tlyric = tlyric_w.read().decode('utf-8')  #获取歌词文件

            if(song == "nothing"):  #当直接用id点歌时
                ass_maker.make_ass(filename,'当前歌曲网易云id：'+str(s)+"\\N点播人："+user,path,lyric,tlyric)  #生成字幕
                ass_maker.make_info(filename,'id：'+str(s)+",点播人："+user,path)    #生成介绍信息，用来查询
            else:   #当用关键字搜索点歌时
                ass_maker.make_ass(filename,'当前网易云id：'+str(s)+"\\N点播关键词："+song+"\\N点播人："+user,path,lyric,tlyric)   #生成字幕
                ass_maker.make_info(filename,'id：'+str(s)+",关键词："+song+",点播人："+user,path)    #生成介绍信息，用来查询
            send_dm_long(t+str(s)+'下载完成，已加入播放队列')
            print('[log]已添加排队项目：'+t+str(s))
        elif(t == 'mv'):    #当参数为mv时
            urllib.request.urlretrieve(url, path+'/downloads/'+filename+'.mp4') #下载mv
            if(song == "nothing"):  #当直接用id点mv时
                ass_maker.make_ass(filename+'ok','当前MV网易云id：'+str(s)+"\\N点播人："+user,path)#生成字幕
                ass_maker.make_info(filename+'ok','MVid：'+str(s)+",点播人："+user,path)#生成介绍信息，用来查询
            else:   #当用关键字搜索点mv时
                ass_maker.make_ass(filename+'ok','当前MV网易云id：'+str(s)+"\\NMV点播关键词："+song+"\\N点播人："+user,path)#生成字幕
                ass_maker.make_info(filename+'ok','MVid：'+str(s)+",关键词："+song+",点播人："+user,path)#生成介绍信息，用来查询
            send_dm_long(t+str(s)+'下载完成，等待渲染')
            while (encode_lock):    #渲染锁，如果现在有渲染任务，则无限循环等待
                time.sleep(1)   #等待
            encode_lock = True  #进入渲染，加上渲染锁，防止其他视频一起渲染
            send_dm_long(t+str(s)+'正在渲染')
            os.system('ffmpeg -i "'+path+'/downloads/'+filename+'.mp4" -aspect 16:9 -vf "scale=1280:720, ass='+path+"/downloads/"+filename+'ok.ass'+'" -c:v libx264 -preset ultrafast -maxrate '+var_set.maxbitrate+'k -tune fastdecode -acodec aac -b:a 192k "'+path+'/downloads/'+filename+'rendering.flv"')
            encode_lock = False #关闭渲染锁，以便其他任务继续渲染
            del_file(filename+'.mp4')   #删除渲染所用的原文件
            os.rename(path+'/downloads/'+filename+'rendering.flv',path+'/downloads/'+filename+'ok.flv') #重命名文件，标记为渲染完毕（ok）
            send_dm_long(t+str(s)+'渲染完毕，已加入播放队列')
        try:    #记录日志，已接近废弃
            log_file = open(path+'/songs.log', 'a')
            log_file.writelines(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + ','+user+','+t+str(s)+'\r\n')
            log_file.close()
        except:
            print('[error]log error')
    except: #下载出错
        send_dm_long('出错了：请检查命令或重试')
        print('[log]下载文件出错：'+t+str(s)+',url:'+url)
        del_file(filename+'.mp3')
        del_file(filename+'.mp4')
        del_file(filename+'.flv')
    return url

#下载歌单
def playlist_download(id,user):
    params = urllib.parse.urlencode({'playlist': str(id)}) #格式化参数
    f = urllib.request.urlopen(download_api_url + "?%s" % params)   #设定获取的网址
    try:
        playlist = json.loads(f.read().decode('utf-8'))  #获取结果，并反序化
        send_dm_long('正在下载歌单：'+playlist['playlist']['name']+'，共'+str(len(playlist['playlist']['tracks']))+'首')
    except Exception as e:  #防炸
        print('shit')
        print(e)
        send_dm_long('出错了：请检查命令或重试')
    for song in playlist['playlist']['tracks']:
        print('name:'+song['name']+'id:'+str(song['id']))
        get_download_url(song['id'], 'id', user, song['name'])

    

#下载b站番剧视频，传入值：网址、点播人用户名
def download_bilibili(video_url,user):
    global encode_lock  #视频渲染锁，用来排队
    if(clean_files()):  #检查空间是否在设定值以内，并自动删除多余视频缓存
        send_dm_long('树莓存储空间已爆炸，请联系up')
        return
    try:
        print('[log]downloading bilibili video:'+str(video_url))
        video_info = json.loads(os.popen('you-get '+video_url+' --json').read())    #获取视频标题，标题错误则说明点播参数不对，跳到except
        video_title = video_info['title']   #获取标题
        send_dm_long('正在下载'+video_title)
        #send_dm('注意，视频下载十分费时，请耐心等待')
        filename = str(time.mktime(datetime.datetime.now().timetuple()))    #用时间戳设定文件名
        os.system('you-get '+video_url+' --format=flv -o '+path+'/downloads -O '+filename+'rendering1') #下载视频文件
        ass_maker.make_ass(filename+'ok',"点播人："+user+"\\N番剧："+video_title+"\\N"+video_url,path) #生成字幕
        ass_maker.make_info(filename+'ok','番剧：'+video_title+",点播人："+user,path)  #生成介绍信息，用来查询
        send_dm_long('番剧'+video_title+'下载完成，等待渲染')
        while (encode_lock):    #渲染锁，如果现在有渲染任务，则无限循环等待
            time.sleep(1)   #等待
        encode_lock = True  #进入渲染，加上渲染锁，防止其他视频一起渲染
        send_dm_long('番剧'+video_title+'正在渲染')
        os.system('ffmpeg -i "'+path+'/downloads/'+filename+'rendering1.flv" -aspect 16:9 -vf "scale=1280:720, ass='+path+"/downloads/"+filename+'ok.ass'+'" -c:v libx264 -preset ultrafast -maxrate '+var_set.maxbitrate+'k -tune fastdecode -acodec aac -b:a 192k "'+path+'/downloads/'+filename+'rendering.flv"')
        encode_lock = False #关闭渲染锁，以便其他任务继续渲染
        del_file(filename+'rendering1.flv') #删除渲染所用的原文件
        os.rename(path+'/downloads/'+filename+'rendering.flv',path+'/downloads/'+filename+'ok.flv') #重命名文件，标记为渲染完毕（ok）
        send_dm_long('番剧'+video_title+'渲染完毕，已加入播放队列')
    except: #报错提示，一般只会出现在获取标题失败时出现，就是点播参数不对
        send_dm_long('出错了：请检查命令或重试')
        
#下载b站任意视频，传入值：网址、点播人用户名
#此部分逻辑与“下载b站番剧视频”部分完全相同，不另行作注释解释
def download_av(video_url,user):
    global encode_lock
    if(clean_files()):
        send_dm_long('树莓存储空间已爆炸，请联系up')
        return
    try:
        v_format = 'flv'
        print('[log]downloading bilibili video:'+str(video_url))
        video_info = json.loads(os.popen('you-get '+video_url+' --json').read())
        video_title = video_info['title']
        send_dm_long('正在下载'+video_title)
        #send_dm('注意，视频下载十分费时，请耐心等待')
        filename = str(time.mktime(datetime.datetime.now().timetuple()))
        os.system('you-get '+video_url+' -o '+path+'/downloads -O '+filename+'rendering1')
        print('you-get '+video_url+' -o '+path+'/downloads -O '+filename+'rendering1')
        if(os.path.isfile(path+'/downloads/'+filename+'rendering1.flv')):
            v_format = 'flv'
        elif(os.path.isfile(path+'/downloads/'+filename+'rendering1.mp4')):
            v_format = 'mp4'
        else:
            send_dm_long('视频'+video_title+'下载失败，请重试')
            return
        ass_maker.make_ass(filename+'ok','点播人：'+user+"\\N视频："+video_title+"\\N"+video_url,path)
        ass_maker.make_info(filename+'ok','视频：'+video_title+",点播人："+user,path)
        send_dm_long('视频'+video_title+'下载完成，等待渲染')
        while (encode_lock):
            time.sleep(1)
        encode_lock = True
        send_dm_long('视频'+video_title+'正在渲染')
        os.system('ffmpeg -i "'+path+'/downloads/'+filename+'rendering1.'+v_format+'" -aspect 16:9 -vf "scale=1280:720, ass='+path+"/downloads/"+filename+'ok.ass'+'" -c:v libx264 -preset ultrafast -maxrate '+var_set.maxbitrate+'k -tune fastdecode -acodec aac -b:a 192k "'+path+'/downloads/'+filename+'rendering.flv"')
        encode_lock = False
        del_file(filename+'rendering1.'+v_format)
        os.rename(path+'/downloads/'+filename+'rendering.flv',path+'/downloads/'+filename+'ok.flv')
        send_dm_long('视频'+video_title+'渲染完毕，已加入播放队列')
    except:
        send_dm_long('出错了：请检查命令或重试')

#搜索歌曲并下载
def search_song(s,user):
    print('[log]searching song:'+s)
    params = urllib.parse.urlencode({'type': 1, 's': s})    #格式化参数
    f = urllib.request.urlopen("http://s.music.163.com/search/get/?%s" % params)    #设置接口网址
    search_result = json.loads(f.read().decode('utf-8'))    #获取结果
    result_id = search_result["result"]["songs"][0]["id"]   #提取歌曲id
    _thread.start_new_thread(get_download_url, (result_id, 'id', user,s))   #扔到下载那里下载

#搜索mv并下载
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
    req = urllib.request.Request(url,postdata,header)   #设置接口网址
    result = json.loads(urllib.request.urlopen(req).read().decode('utf-8')) #获取结果
    result_id = result['result']['mvs'][0]['id']    #提取mv id
    _thread.start_new_thread(get_download_url, (result_id, 'mv', user,s))   #扔到下载那里下载

#切歌请求次数统计
jump_to_next_counter = 0
rp_lock = False
def pick_msg(s, user):
    global jump_to_next_counter #切歌请求次数统计
    global encode_lock  #视频渲染任务锁
    global rp_lock
    if ((user=='晨旭') | (user=='摘希喵喵喵')):    #debug使用，请自己修改
        if(s=='锁定'):
            rp_lock = True
            send_dm_long('已锁定点播功能，不响应任何弹幕')
        if(s=='解锁'):
            rp_lock = False
            send_dm_long('已解锁点播功能，开始响应弹幕请求')
    if((user == '接待喵') | rp_lock):  #防止自循环
        return
    #下面的不作解释，很简单一看就懂
    if(s.find('mvid+') == 0):
        send_dm_long('已收到'+user+'的指令')
        s = s.replace(' ', '')   #剔除弹幕中的所有空格
        _thread.start_new_thread(get_download_url, (s.replace('mvid+', '', 1), 'mv',user))
    elif (s.find('mv+') == 0):
        try:
            send_dm_long('已收到'+user+'的指令')
            search_mv(s.replace('mv+', '', 1),user)
        except:
            print('[log]mv not found')
            send_dm_long('出错了：没这mv')
    elif (s.find('song+') == 0):
        try:
            send_dm_long('已收到'+user+'的指令')
            search_song(s.replace('song+', '', 1),user)
        except:
            print('[log]song not found')
            send_dm_long('出错了：没这首歌')
    elif (s.find('id+') == 0):
        send_dm_long('已收到'+user+'的指令')
        s = s.replace(' ', '')   #剔除弹幕中的所有空格
        _thread.start_new_thread(get_download_url, (s.replace('id+', '', 1), 'id',user))
    elif(s.find('mvid') == 0):
        send_dm_long('已收到'+user+'的指令')
        s = s.replace(' ', '')   #剔除弹幕中的所有空格
        _thread.start_new_thread(get_download_url, (s.replace('mvid', '', 1), 'mv',user))
    elif (s.find('mv') == 0):
        try:
            send_dm_long('已收到'+user+'的指令')
            search_mv(s.replace('mv', '', 1),user)
        except:
            print('[log]mv not found')
            send_dm_long('出错了：没这mv')
    elif (s.find('song') == 0):
        try:
            send_dm_long('已收到'+user+'的指令')
            search_song(s.replace('song', '', 1),user)
        except:
            print('[log]song not found')
            send_dm_long('出错了：没这首歌')
    elif (s.find('id') == 0):
        send_dm_long('已收到'+user+'的指令')
        s = s.replace(' ', '')   #剔除弹幕中的所有空格
        _thread.start_new_thread(get_download_url, (s.replace('id', '', 1), 'id',user))
    elif (s.find('点歌') == 0):
        try:
            send_dm_long('已收到'+user+'的指令')
            search_song(s.replace('点歌', '', 1),user)
        except:
            print('[log]song not found')
            send_dm_long('出错了：没这首歌')
    elif (s.find('喵') > -1):
        replay = ["喵？？", "喵喵！", "喵。。喵？", "喵喵喵~", "喵！"]
        send_dm_long(replay[random.randint(0, len(replay))])  #用于测试是否崩掉
    elif (s == '切歌'):   #切歌请求
        if(encode_lock):    #切歌原理为killall ffmpeg，但是如果有渲染任务，kill后也会结束渲染进程，会出错
            send_dm_long('有渲染任务，无法切歌')
            return
        jump_to_next_counter += 1   #切歌次数统计加一
        if((user=='晨旭') | (user=='摘希喵喵喵')): #debug使用，请自己修改
            jump_to_next_counter=5
        if(jump_to_next_counter < 5):   #次数未达到五次
            send_dm_long('已收到'+str(jump_to_next_counter)+'次切歌请求，达到五次将切歌')
        else:   #次数未达到五次
            jump_to_next_counter = 0    #次数统计清零
            send_dm_long('已执行切歌动作')
            os.system('killall ffmpeg') #强行结束ffmpeg进程
    elif ((s == '点播列表') or (s == '歌曲列表')):
        send_dm_long('已收到'+user+'的指令，正在查询')
        files = os.listdir(path+'/downloads')   #获取目录下所有文件
        files.sort()    #按文件名（下载时间）排序
        songs_count = 0 #项目数量
        all_the_text = ""
        for f in files:
            if((f.find('.mp3') != -1) and (f.find('.download') == -1)): #如果是mp3文件
                try:
                    info_file = open(path+'/downloads/'+f.replace(".mp3",'')+'.info', 'r')  #读取相应的info文件
                    all_the_text = info_file.read()
                    info_file.close()
                except Exception as e:
                    print(e)
                if(songs_count < 10):
                    send_dm_long(all_the_text)
                songs_count += 1
            if((f.find('ok.flv') != -1) and (f.find('.download') == -1) and (f.find('rendering') == -1)):#如果是有ok标记的flv文件
                try:
                    info_file = open(path+'/downloads/'+f.replace(".flv",'')+'.info', 'r')  #读取相应的info文件
                    all_the_text = info_file.read()
                    info_file.close()
                except Exception as e:
                    print(e)
                if(songs_count < 10):
                    send_dm_long(all_the_text)
                songs_count += 1
        if(songs_count <= 10):
            send_dm_long('点播列表展示完毕，一共'+str(songs_count)+'个')
        else:
            send_dm_long('点播列表前十个展示完毕，一共'+str(songs_count)+'个')
    elif (s == '渲染列表'):
        send_dm_long('已收到'+user+'的指令，正在查询')
        files = os.listdir(path+'/downloads')   #获取目录下所有文件
        files.sort()    #按文件名（下载时间）排序
        songs_count = 0 #项目数量
        all_the_text = ""
        for f in files:
            if(f.find('rendering1.flv') != -1): #如果是没有ok标记的flv文件
                try:
                    info_file = open(path+'/downloads/'+f.replace("rendering1.flv",'')+'ok.info', 'r')  #读取相应的info文件
                    all_the_text = info_file.read()
                    info_file.close()
                except Exception as e:
                    print(e)
                if(songs_count < 5):
                    send_dm_long(all_the_text)
                songs_count += 1
            if(f.find('.mp4') != -1):   #如果是mp4文件
                try:
                    info_file = open(path+'/downloads/'+f.replace(".mp4",'')+'ok.info', 'r')    #读取相应的info文件
                    all_the_text = info_file.read()
                    info_file.close()
                except Exception as e:
                    print(e)
                if(songs_count < 5):
                    send_dm_long(all_the_text)
                songs_count += 1
        if(songs_count <= 5):
            send_dm_long('渲染列表展示完毕，一共'+str(songs_count)+'个')
        else:
            send_dm_long('渲染列表前5个展示完毕，一共'+str(songs_count)+'个')
    elif (s.find('番剧') == 0):
        send_dm_long('您的直播间因“禁止盗播新番”，已被管x员“切断”，请更改直播内容。')
        return
        try:
            send_dm_long('已收到'+user+'的指令')
            #番剧网址格式：https://bangumi.bilibili.com/anime/123/play#456
            ture_url=s.replace('.','/play#')
            ture_url=ture_url.replace('番剧','https://bangumi.bilibili.com/anime/')
            _thread.start_new_thread(download_bilibili, (ture_url,user))
        except:
            print('[log]video not found')
    elif (s.find('av') == 0):
        s = s.replace(' ', '')   #剔除弹幕中的所有空格
        try:
            if(s.find('p') == -1):
                send_dm_long('已收到'+user+'的指令')
                #视频网址格式：https://www.bilibili.com/video/avxxxxx
                ture_url=s.replace('av','https://www.bilibili.com/video/av')
                _thread.start_new_thread(download_av, (ture_url,user))
            else:
                send_dm_long('已收到'+user+'的指令')
                #视频网址格式：https://www.bilibili.com/video/avxxxx/#page=x
                ture_url=s.replace('p','/#page=')
                ture_url=ture_url.replace('av','https://www.bilibili.com/video/av')
                _thread.start_new_thread(download_av, (ture_url,user))
        except:
            print('[log]video not found')
    elif (s.find('温度') > -1):
        send_dm_long("CPU "+os.popen('vcgencmd measure_temp').readline())   #读取命令行得到的温度
        try:
            temp = dht11.get_dht11()
            send_dm_long("温度："+str(temp[0])+"℃，湿度："+str(temp[1])+"%")
        except Exception as e:  #防炸
            print('shit')
            print(e)
            send_dm_long("温湿度获取失败")
    elif (s.find('歌单') == 0):
        send_dm_long('已收到'+user+'的指令')
        s = s.replace(' ', '')   #剔除弹幕中的所有空格
        _thread.start_new_thread(playlist_download, (s.replace('歌单', '', 1),user))
    # else:
    #     print('not match anything')





#发送弹幕函数，通过post完成，具体可以自行使用浏览器，进入审查元素，监控network选项卡研究
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
    
#每条弹幕最长只能发送20字符，过长的弹幕分段发送
def send_dm_long(s):
    n=var_set.dm_size
    for hx in sensitive_word:                  #处理和谐词，防止点播机的回复被和谐
        if (s.find(hx) > -1):
            s = s.replace(hx, hx[0]+"-"+hx[1:])    #在和谐词第一个字符后加上一个空格
    for i in range(0, len(s), n):
        send_dm(s[i:i+n])

#获取原始弹幕数组
#本函数不作注释，具体也请自己通过浏览器审查元素研究
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

#检查某弹幕是否与前一次获取的弹幕数组有重复
def check_dm(dm):
    global temp_dm
    for t_get in temp_dm['data']['room']:
        if((t_get['text'] == dm['text']) & (t_get['timeline'] == dm['timeline'])):
            return False
    return True

#弹幕获取函数，原理为不断循环获取指定直播间的初始弹幕，并剔除前一次已经获取到的弹幕，余下的即为新弹幕
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
                #text = t_get['text'].replace('-', '')   #剔除弹幕中的所有空格
                pick_msg(text,t_get['nickname'])   #新弹幕检测是否匹配为命令
        temp_dm = dm_result
        time.sleep(1)

def test():
    print('ok')

print('程序已启动，连接房间id：'+roomid)
send_dm_long('弹幕监控已启动，可以点歌了')
while True: #防炸
    try:
        get_dm_loop()   #开启弹幕获取循环函数
    except Exception as e:  #防炸
        print('shit')
        print(e)
        dm_lock = False #解开弹幕锁，以免因炸了而导致弹幕锁没解开，进而导致一直锁着发不出弹幕
