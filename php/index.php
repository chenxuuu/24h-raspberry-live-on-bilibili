<?php
require_once 'NeteaseMusicAPI_mini.php';
function get_url_id($id)
{
    $api = new NeteaseMusicAPI();
    $result = $api->url($id);
    $data=json_decode($result, true);
    return $data['data'][0]['url'];
}
function get_url_mv($id)
{
    $api = new NeteaseMusicAPI();
    $result = $api->mv($id);
    $data=json_decode($result, true);
    $vurl = $data['data']['brs']['720'];
    if($vurl == null)
    {
        $vurl = $data['data']['brs']['480'];
    }
    return $vurl;
}
function get_lyric($id)
{
    $api = new NeteaseMusicAPI();
    $result = $api->lyric($id);
    $data=json_decode($result, true);
    return $data['lrc']['lyric'];
}
function get_tlyric($id)
{
    $api = new NeteaseMusicAPI();
    $result = $api->lyric($id);
    $data=json_decode($result, true);
    return $data['tlyric']['lyric'];
}

if(!empty($_GET['debug']))
{
    if(!empty($_GET['id']))
    {
        $api = new NeteaseMusicAPI();
        $result = $api->url($_GET['id']);
        echo $result;
    }
    elseif(!empty($_GET['mv']))
    {
        $api = new NeteaseMusicAPI();
        $result = $api->mv($_GET['mv']);
        echo $result;
    }
    elseif(!empty($_GET['lyric']))
    {
        $api = new NeteaseMusicAPI();
        $result = $api->lyric($_GET['lyric']);
        echo $result;
    }
    elseif(!empty($_GET['tlyric']))
    {
        $api = new NeteaseMusicAPI();
        $result = $api->lyric($_GET['tlyric']);
        echo $result;
    }
}
elseif(!empty($_GET['id']))
{
    echo get_url_id($_GET['id']);
}
elseif(!empty($_GET['mv']))
{
    echo get_url_mv($_GET['mv']);
}
elseif(!empty($_GET['lyric']))
{
    echo get_lyric($_GET['lyric']);
}
elseif(!empty($_GET['tlyric']))
{
    echo get_tlyric($_GET['tlyric']);
}
else
{
    echo 'nothing';
}
?>