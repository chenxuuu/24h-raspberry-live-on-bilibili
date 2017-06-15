<head>
<meta charset="utf-8">
</head>
<body>
<form action="" method="post">
<p>一个简陋的点歌台23333</p>
<p>搜索结果来自网易云</p>
<!--<p>输入歌曲名搜索歌曲：<input type="text" name="song" /></p>
<p><input type="submit" name="sub" value="搜索" /></p>-->
</form>
<form action="" method="post">
<p>直接输入网易云id点歌<br/>实例（红色部分为id）：<br/>http://music.163.com/song/<font color="red">26489014</font>/?userid=261620056<br/>http://music.163.com/#/song?id=<font color="red">32477053</font></p>
<p>id：<input type="text" name="id" /></p>
<p><input type="submit" name="sub" value="查看" /></p>
</form>
<a href="https://www.chenxublog.com/2017/06/05/raspi-live-24h-bilibili-choice.html" target="_blank">by 晨旭/chenxublog.com | 网站运行基于树莓派2B</a><br/>
直播间地址：<a href="http://live.bilibili.com/16703" target="_blank">http://live.bilibili.com/16703</a><br/>
提交意见或建议：<a href="https://github.com/chenxuuu/24h-raspberry-live-on-bilibili/issues" target="_blank">https://github.com/chenxuuu/24h-raspberry-live-on-bilibili/issues</a><br/><br/><br/>
当前状态：<div id='t'></div>
<?php
require_once 'NeteaseMusicAPI_mini.php';

function get_url_id($id)
{
    $api = new NeteaseMusicAPI();
    $result = $api->url($id);
    $result = str_replace("[","",$result);
    $result = str_replace("]","",$result);
    $data=json_decode($result, true);
    return $data['data']['url'];
}
function fuckcheck($id)
{
    $html=file_get_contents('http://music.163.com/song/'.$id);
    
    return !(strpos($html,'戏曲') || strpos($html,'评书') || strpos($html,'相声') || strpos($html,'戏剧') || strpos($html,'国粹') || strpos($html,'京剧') || strpos($html,'豫剧') || strpos($html,'昆曲'));
}
function idcheck($id)
{
    $counttemp=0;
    for($counttemp=1;$counttemp<31;$counttemp++)
    {
        if (file_exists($counttemp.'.now') && $id==file_get_contents($counttemp.'.now'))   
        {   
            return false;
        }
    }
    $counttemp=0;
    for($counttemp=1;$counttemp<31;$counttemp++)
    {
        if (file_exists($counttemp.'.id') && $id==file_get_contents($counttemp.'.id'))   
        {   
            return false;
        }
    }
    return true;
}
function netease_http($url)
{
    $refer = "http://music.163.com/";
    $header[] = "Cookie: " . "appver=1.5.0.75771;";
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_HTTPHEADER, $header);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_BINARYTRANSFER, true);
    curl_setopt($ch, CURLOPT_REFERER, $refer);
    $cexecute = curl_exec($ch);
    curl_close($ch);
    if ($cexecute)
    {
        $result = json_decode($cexecute, true);
        return $result;
    }
    else
    {
        return false;
    }
}
function getStatus($url){
    if($headers = @get_headers($url)){
            $status  = $headers[0];
            $statusno= false;
            if(preg_match_all('%HTTP/1\.1 ([\d]{3})%i',$status,$matches)){
                    $statusno = $matches[1][0];
            }
            return $statusno;
    }
        return false;
}

if(!empty($_POST['song'])){

$song=$_POST['song'];
echo '搜索关键词：'.$song.'<br/>=========================================================<br/>';
$url = "http://s.music.163.com/search/get/?type=1&s=".$song;
$response = netease_http($url);
$counttemp=0;
for($counttemp=0;$counttemp<10;$counttemp++)
{
    if(getStatus($response['result']['songs'][$counttemp]['audio'])=='200')
    {
        echo $response['result']['songs'][$counttemp]['name'].'<img src="'.$response['result']['songs'][$counttemp]['album']['picUrl'].'" height="100"/><a href="?down='.$response['result']['songs'][$counttemp]['audio'].'">就选这首了</a><br/>试听：<audio src="'.$response['result']['songs'][$counttemp]['audio'].'" controls="controls"></audio><br/>=========================================================<br/>';
    }
    else
    {
        echo '第'.($counttemp+1).'首歌曲获取失败（歌曲失效/版权问题/网络抽风）<br/>=========================================================<br/>';
    }
}

}
elseif(!empty($_POST['id'])){
    echo '<font color="red">请遵守秩序，不要重复点同一首歌！</font>）：<br/>';
    echo '试听：<audio src="'.get_url_id($_POST['id']).'" controls="controls"></audio><br/><a href="?down='.get_url_id($_POST['id']).'&id='.$_POST['id'].'">就选这首了</a>';
}
elseif(!empty($_GET['down']) && !empty($_GET['id']) && empty($_GET['write']) && strpos($_GET['down'],"music.126.net")!=false)
{
    if(getStatus($_GET['down'])!='200')
    {
        echo '获取到的链接可能有点问题，请再次提交试试。';
        return;
    }
    echo '当前可供选择的空闲的序列（注意，直播是从第1首到第30首按顺序播放的。<font color="red">歌曲长度最大限制十分钟，超过将丢弃</font>）：<br/>';
    $counttemp=0;
    for($counttemp=1;$counttemp<31;$counttemp++)
    {
        if($counttemp%5==0)
        {
            echo '<br/>';
        }
        if (!file_exists($counttemp.'.txt') && !file_exists($counttemp.'.233'))
        {
            echo '<a href="?write='.$counttemp.'&down='.$_GET['down'].'&id='.$_GET['id'].'">换掉第'.$counttemp.'首歌</a>（<font color="green">可以换歌</font>）|';
        }
        elseif(!file_exists($counttemp.'.233'))
        {
            echo '第'.$counttemp.'首歌（<font color="red">排队渲染中</font>）|';
        }
        else
        {
            echo '第'.$counttemp.'首歌（<font color="red">被晨旭锁定</font>）|';
        }
    }
    

}
elseif(!empty($_GET['write']) && !empty($_GET['down']) && !empty($_GET['id']))
{
    if(getStatus($_GET['down'])!='200')
    {
        echo '获取到的链接可能有点问题，请再次提交试试。';
        return;
    }
    
    if(file_exists($_GET['write'].'.txt'))
    {
        echo '啊哦！这个序号已经有人选中了！正在渲染！';
    }
    elseif(!idcheck($_GET['id']))
    {
        echo '<font color="red">请遵守秩序，不要重复点同一首歌！</font>';
    }
    // elseif(!fuckcheck($_GET['id']))
    // {
        // echo '<font size="7" style="font-family:微软雅黑">你是有病吗？</font>';
    // }
    elseif(!file_exists($_GET['write'].'.233'))
    {
        $myfile = fopen($_GET['write'].'.txt', "w") or die("Unable to open file1!");
        fwrite($myfile, $_GET['down']);
        fclose($myfile);
        
        $myfile1 = fopen($_GET['write'].'.id', "w") or die("Unable to open file2!");
        fwrite($myfile1, $_GET['id']);
        fclose($myfile1);
        
        $myfile2 = fopen('log.html', "a") or die("Unable to open file3!");
        fwrite($myfile2, date("y/m/d").' '.date("h:i:sa").' 第'.$_GET['write'].'首歌被换为<a href="http://music.163.com/#/song/'.$_GET['id'].'" target="_blank">'.$_GET['id'].'</a><br/>');
        fclose($myfile2);
        
        echo '第'.$_GET['write'].'首歌曲的渲染请求提交成功！<a href="index.php">返回首页</a>';
    }
}
else
{
    echo '树莓当前负载状态（注意，直播是从第1首到第30首按顺序播放的。<font color="red">当相同曲目的播放与渲染任务同时进行时直播会崩溃，请不要这样做</font>）：<br/>';
    $counttemp=0;
    for($counttemp=1;$counttemp<31;$counttemp++)
    {
        if($counttemp%5==0)
        {
            echo '<br/>';
        }
        if (!file_exists($counttemp.'.txt') && !file_exists($counttemp.'.233'))
        {
            echo '第'.$counttemp.'首歌：<a href="http://music.163.com/song/'.file_get_contents($counttemp.'.now').'" target="_blank">'.file_get_contents($counttemp.'.now').'</a>（<font color="green">可以换掉</font>）|';
        }
        elseif(!file_exists($counttemp.'.233'))
        {
            echo '第'.$counttemp.'首歌：<a href="http://music.163.com/song/'.file_get_contents($counttemp.'.now').'" target="_blank">'.file_get_contents($counttemp.'.now').'</a>（<font color="red">排队渲染中，会被换为：<a href="http://music.163.com/song/'.file_get_contents($counttemp.'.id').'" target="_blank">'.file_get_contents($counttemp.'.id').'</a></font>）|';
        }
        else
        {
            echo '第'.$counttemp.'首歌：<a href="http://music.163.com/song/'.file_get_contents($counttemp.'.now').'" target="_blank">'.file_get_contents($counttemp.'.now').'</a>（<font color="red">被晨旭锁定</font>）|';
        }
    }
    //echo '<br><iframe src="http://wfkj1.papapoi.com/songs/log.html" width="500" height="200"></iframe>';
}

?>
<script type="text/javascript" src="now.js"></script>
<a href="http://wfkj1.papapoi.com/songs/log.html" target="_blank">查看点歌日志</a>
<font size="7" style="font-family:微软雅黑">
<h3>
如果有不想听到的歌曲<br/>
请复制歌曲id并给我发送b站私信<br/>
我会看情况禁止该id歌曲的点播<br/>
感谢反馈！大家的反馈会使点歌台的功能更加完善！
</h3>
</font>
</body>