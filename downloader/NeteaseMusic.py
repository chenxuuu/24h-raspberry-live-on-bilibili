from util.Request import Request
from util.AES import AESCipher
import json
import time

class NeteaseMusic(object):

    def __init__(self):
        self.config = {
            'nonce': '0CoJUm6Qyw8W8jud',
            'secretKey': 'TA3YiYCfY2dDJQgg',
            'encSecKey': '84ca47bca10bad09a6b04c5c927ef077d9b9f1e37098aa3eac6ea70eb59df0aa28b691b7e75e4f1f9831754919ea784c8f74fbfadf2898b0be17849fd656060162857830e241aba44991601f137624094c114ea8d17bce815b0cd4e5b8e2fbaba978c6d1d14dc3d1faf852bdd28818031ccdaaa13a6018e1024e2aae98844210',
            'IV': '0102030405060708'
        }

    # aes-128-cbc
    def aesEncode(self, data, key):
        return AESCipher(key=key).encrypt(data, self.config['IV'])
    
    # 预处理Post数据
    def prepare(self, data):
        result = { 'params': self.aesEncode(json.dumps(data), self.config['nonce']) }
        result['params'] = self.aesEncode(result['params'], self.config['secretKey'])
        result['encSecKey'] = self.config['encSecKey']
        return result

    # 搜索歌曲
    def search(self, keyword, singer=None):
        response = Request.jsonGet(url='http://s.music.163.com/search/get/', params={
            'type': 1,
            's': keyword
        })
        if 'code' in response and response['code'] == 200:
            result = []
            # 遍历歌曲
            for song in response['result']['songs']:
                # 遍历歌手
                song['singer'] = ''
                isSelect = True
                for artist in song['artists']:
                    if singer and artist['name'] == singer:
                        song['singer'] = singer
                        isSelect = True
                    elif singer:
                        isSelect = False
                    else:
                        isSelect = True
                        song['singer'] += artist['name'] + ' '
                if isSelect:
                    song['singer'] = song['singer'].strip()
                    result.append(song)

            return result
        else:
            return []
    
    # 搜索歌曲 取第一首
    def searchSingle(self, keyword, singer=None):
        result = self.search(keyword, singer)
        if result:
            return result[0]
        else:
            return None

    # 批量获取歌曲链接
    def getUrl(self, songIds):
        response = Request.jsonPost(url='http://music.163.com/weapi/song/enhance/player/url?csrf_token=', params=self.prepare({
            'ids': songIds,
            'br': 999000,
            'csrf_token': ''
        }))

        # 解析response
        if 'code' in response and response['code'] == 200:
            if 'data' in response:
                return response['data']
            else:
                return []
        else:
            return None
    
    # 获取单一歌曲链接
    def getSingleUrl(self, songId):
        result = self.getUrl([songId])
        if result == None:
            return result
        elif len(result) == 0:
            return {}
        else:
            return result[0]

    # 通过歌曲id下载歌曲
    def download(self, songId, filename=None, callback=None):
        # 名称处理
        if not filename:
            filename = str(int(time.time()))

        # 获取歌曲并下载
        musicResult = self.getSingleUrl(songId)
        if musicResult and 'url' in musicResult:
            musicUrl = musicResult['url']
            filename = './downloader/download/%s.mp3' % filename
            Request.download(musicUrl, filename, callback)

            return filename
        else:
            return False

    # 通过ID获取歌曲信息
    def getInfo(self, id):
        response = Request.jsonPost(url='http://music.163.com/weapi/v3/song/detail?csrf_token=', params=self.prepare({
            'c': json.dumps([{ 'id': id }]),
            'csrf_token': ''
        }))
        if 'code' in response and response['code'] == 200:
            if 'songs' in response and response['songs']:
                song = response['songs'][0]
                return {
                    'id': song['id'],
                    'name': song['name'],
                    'singer': song['ar'][0]['name']
                }
                pass
            else:
                return False
        else:
            return False

    # 获取歌词
    def getLyric(self, songId):
        response = Request.jsonPost(url='http://music.163.com/weapi/song/lyric?csrf_token=', params=self.prepare({
            'id': songId,
            'os': 'pc',
            'lv': -1,
            'kv': -1,
            'tv': -1,
            'csrf_token': ''
        }))

        if 'code' in response and response['code'] == 200:
            result = {
                'lyric': '',
                'tlyric': ''
            }
            # 获取歌词
            if 'lrc' in response and 'lyric' in response['lrc']:
                result['lyric'] = response['lrc']['lyric']
            else:
                return False

            # 获取翻译歌词
            if 'tlyric' in response and 'lyric' in response['tlyric']:
                result['tlyric'] = response['tlyric']['lyric']

            return result
        else:
            return False