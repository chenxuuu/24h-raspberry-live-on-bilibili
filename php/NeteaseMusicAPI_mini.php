<?php
/*!
 * Netease Cloud Music Api - mini
 * https://i-meto.com
 * Version 3.0.0
 *
 * Copyright 2016, METO
 * Released under the MIT license
 */




class NeteaseMusicAPI{

    // General
    protected $_MINI_MODE=false;
    protected $_MODULUS='00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7';
    protected $_NONCE='0CoJUm6Qyw8W8jud';
    protected $_PUBKEY='010001';
    protected $_VI='0102030405060708';
    protected $_USERAGENT='Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.157 Safari/537.36';
    protected $_COOKIE='os=pc; osver=Microsoft-Windows-10-Professional-build-10586-64bit; appver=2.0.3.131777; channel=netease; __remember_me=true';
    protected $_REFERER='http://music.163.com/';
    // use static secretKey, without RSA algorithm
    protected $_secretKey='TA3YiYCfY2dDJQgg';
    protected $_encSecKey='84ca47bca10bad09a6b04c5c927ef077d9b9f1e37098aa3eac6ea70eb59df0aa28b691b7e75e4f1f9831754919ea784c8f74fbfadf2898b0be17849fd656060162857830e241aba44991601f137624094c114ea8d17bce815b0cd4e5b8e2fbaba978c6d1d14dc3d1faf852bdd28818031ccdaaa13a6018e1024e2aae98844210';

    // encrypt mod
    protected function prepare($raw){
        $data['params']=$this->aes_encode(json_encode($raw),$this->_NONCE);
        $data['params']=$this->aes_encode($data['params'],$this->_secretKey);
        $data['encSecKey']=$this->_encSecKey;
        return $data;
    }
    protected function aes_encode($secretData,$secret){
        return openssl_encrypt($secretData,'aes-128-cbc',$secret,false,$this->_VI);
    }

    // CURL
    protected function curl($url,$data=null){
        $curl=curl_init();
        curl_setopt($curl,CURLOPT_URL,$url);
        if($data){
            if(is_array($data))$data=http_build_query($data);
            curl_setopt($curl,CURLOPT_POSTFIELDS,$data);
            curl_setopt($curl,CURLOPT_POST,1);
        }
        curl_setopt($curl,CURLOPT_RETURNTRANSFER, 1);
        curl_setopt($curl,CURLOPT_CONNECTTIMEOUT, 10);
        curl_setopt($curl,CURLOPT_REFERER,$this->_REFERER);
        curl_setopt($curl,CURLOPT_COOKIE,$this->_COOKIE);
        curl_setopt($curl,CURLOPT_USERAGENT,$this->_USERAGENT);
        $result=curl_exec($curl);
        curl_close($curl);
        return $result;
    }

    // main function
    public function search($s,$limit=30,$offset=0,$type=1){
        $url='http://music.163.com/weapi/cloudsearch/get/web?csrf_token=';
        $data=array(
            's'=>$s,
            'type'=>$type,
            'limit'=>$limit,
            'total'=>'true',
            'offset'=>$offset,
            'csrf_token'=>'',
        );
        $raw=$this->curl($url,$this->prepare($data));
        if($this->_MINI_MODE){
            $this->_MINI_MODE=false;
            $raw=json_decode($raw,1);
            return json_encode($this->clear_data($raw["result"]["songs"]));
        }
        else return $raw;
    }

    public function artist($artist_id){
        $url='http://music.163.com/weapi/v1/artist/'.$artist_id.'?csrf_token=';
        $data=array(
            'csrf_token'=>'',
        );
        $raw=$this->curl($url,$this->prepare($data));
        if($this->_MINI_MODE){
            $this->_MINI_MODE=false;
            $raw=json_decode($raw,1);
            return json_encode($this->clear_data($raw["hotSongs"]));
        }
        else return $raw;
    }

    public function album($album_id){
        $url='http://music.163.com/weapi/v1/album/'.$album_id.'?csrf_token=';
        $data=array(
            'csrf_token'=>'',
        );
        $raw=$this->curl($url,$this->prepare($data));
        if($this->_MINI_MODE){
            $this->_MINI_MODE=false;
            $raw=json_decode($raw,1);
            return json_encode($this->clear_data($raw["songs"]));
        }
        else return $raw;
    }

    public function detail($song_id){
        $url='http://music.163.com/weapi/v3/song/detail?csrf_token=';
        $data=array(
            'c'=>'['.json_encode(array('id'=>$song_id)).']',
            'csrf_token'=>'',
        );
        $raw=$this->curl($url,$this->prepare($data));
        if($this->_MINI_MODE){
            $this->_MINI_MODE=false;
            $raw=json_decode($raw,1);
            return json_encode($this->clear_data($raw["songs"]));
        }
        else return $raw;
    }

    public function url($song_id,$br=999000){
        $url='http://music.163.com/weapi/song/enhance/player/url?csrf_token=';
        if(!is_array($song_id))$song_id=array($song_id);
        $data=array(
            'ids'=>$song_id,
            'br'=>$br,
            'csrf_token'=>'',
        );
        return $this->curl($url,$this->prepare($data));
    }

    public function playlist($playlist_id){
        $url='http://music.163.com/weapi/v3/playlist/detail?csrf_token=';
        $data=array(
            'id'=>$playlist_id,
            'n'=>1000,
            'csrf_token'=>'',
        );
        $raw=$this->curl($url,$this->prepare($data));
        if($this->_MINI_MODE){
            $this->_MINI_MODE=false;
            $raw=json_decode($raw,1);
            return json_encode($this->clear_data($raw["playlist"]["tracks"]));
        }
        else return $raw;
    }

    public function lyric($song_id){
        $url='http://music.163.com/weapi/song/lyric?csrf_token=';
        $data=array(
            'id'=>$song_id,
            'os'=>'pc',
            'lv'=>-1,
            'kv'=>-1,
            'tv'=>-1,
            'csrf_token'=>'',
        );
        return $this->curl($url,$this->prepare($data));
    }

    public function mv($mv_id){
        $url='http://music.163.com/weapi/mv/detail?csrf_token=';
        $data=array(
            'id'=>$mv_id,
            'csrf_token'=>'',
        );
        return $this->curl($url,$this->prepare($data));
    }

    protected function clear_data($result){
        // you can modify it by yourself, change to your API?!
        foreach($result as $key=>$vo){
            $data[$key]=array(
                'id'=>$key,
                'songid'=>$vo["id"],
                'name'=>$vo["name"],
                'cover'=>'https://p4.music.126.net/'.self::Id2Url($vo['al']["pic_str"]).'/'.$vo['al']["pic_str"].'.jpg',
                'url'=>'http://music.163.com/song/media/outer/url?id='.$vo["id"],
                //'lyric'=>$vo["id"],
                'artist'=>array(),
            );
            foreach($vo['ar'] as $vvo)$data[$key]['artist'][]=$vvo['name'];
            $data[$key]['artist']=implode('/',$data[$key]['artist']);
        }
        return $data;
    }

    public function mini(){
        $this->_MINI_MODE=true;
        return $this;
    }

    /* static url encrypt, use for pic*/
    public function Id2Url($id){
        $byte1[]=$this->Str2Arr('3go8&$8*3*3h0k(2)2');
        $byte2[]=$this->Str2Arr($id);
        $magic=$byte1[0];
        $song_id=$byte2[0];
        for($i=0;$i<count($song_id);$i++)$song_id[$i]=$song_id[$i]^$magic[$i%count($magic)];
        $result=base64_encode(md5($this->Arr2Str($song_id),1));
        $result=str_replace('/','_',$result);
        $result=str_replace('+','-',$result);
        return $result;
    }
    protected function Str2Arr($string){
        $bytes=array();
        for($i=0;$i<strlen($string);$i++)$bytes[]=ord($string[$i]);
        return $bytes;
    }
    protected function Arr2Str($bytes){
        $str='';
        for($i=0;$i<count($bytes);$i++)$str.=chr($bytes[$i]);
        return $str;
    }
}
