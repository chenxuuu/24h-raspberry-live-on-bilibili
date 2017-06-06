<head>
<meta charset="utf-8">
</head>
<body>
<form action="" method="post">
<p>一个简陋的点歌台23333</p>
<p>搜索结果来自网易云</p>
<p>输入歌曲名搜索歌曲：<input type="text" name="song" /></p>
<p><input type="submit" name="sub" value="搜索" /></p>
</form>
<form action="" method="post">
<p>或者直接输入id点歌（推荐！）<br/>实例（红色部分为id）：<br/>http://music.163.com/song/<font color="red">26489014</font>/?userid=261620056<br/>http://music.163.com/#/song?id=<font color="red">32477053</font></p>
<p>id：<input type="text" name="id" /></p>
<p><input type="submit" name="sub" value="查看" /></p>
</form>
by 晨旭/chenxublog.com | running on Raspberry Pi 2 Model B<br/>直播间地址：http://live.bilibili.com/16703<br/><br/><br/>
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
function urlcheck($url)
{
    $counttemp=0;
    for($counttemp=1;$counttemp<31;$counttemp++)
    {
        if (file_exists($counttemp.'.txt') && $url==file_get_contents($counttemp.'.txt'))   
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
    echo '试听：<audio src="'.get_url_id($_POST['id']).'" controls="controls"></audio><br/><a href="?down='.get_url_id($_POST['id']).'">就选这首了</a>';
}
elseif(!empty($_GET['down']) && empty($_GET['write']) && strpos($_GET['down'],"music.126.net")!=false && getStatus($_GET['down'])=='200')
{
    echo '当前可供选择的空闲的序列（注意，直播是从第1首到第30首按顺序播放的。<font color="green">歌曲长度最大限制十分钟，超过将丢弃</font>）：<br/>';
    $counttemp=0;
    for($counttemp=1;$counttemp<31;$counttemp++)
    {
        if($counttemp%5==0)
        {
            echo '<br/>';
        }
        if (!file_exists($counttemp.'.txt'))
        {
            echo '<a href="?write='.$counttemp.'&down='.$_GET['down'].'">换掉第'.$counttemp.'首歌</a>（<font color="green">可以换歌</font>）|';
        }
        else
        {
            echo '第'.$counttemp.'首歌（<font color="red">排队渲染中</font>）|';
        }
    }
}
elseif(!empty($_GET['write']) && !empty($_GET['down']) && urlcheck($_GET['down']) && getStatus($_GET['down'])=='200')
{
    if(!file_exists($_GET['write'].'.txt'))
    {
        //file_put_contents('songs/'.$_GET['write'].'.txt', $_GET['down']);
        $myfile = fopen($_GET['write'].'.txt', "w") or die("Unable to open file!");
        fwrite($myfile, $_GET['down']);
        fclose($myfile);
        echo '第'.$_GET['write'].'首歌曲的渲染请求提交成功！<a href="index.php">返回首页</a>';
    }
    else
    {
        echo '啊哦！这个序号已经有人选中了！正在渲染！';
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
        if (!file_exists($counttemp.'.txt'))
        {
            echo '第'.$counttemp.'首歌（<font color="green">可以换掉</font>）|';
        }
        else
        {
            echo '第'.$counttemp.'首歌（<font color="red">排队渲染中</font>）|';
        }
    }
}

?>
<script type="text/javascript" src="now.js"></script>
</body>