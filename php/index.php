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
    return $data['data']['brs']['720'];
}

if(!empty($_GET['id']))
{
    echo get_url_id($_GET['id']);
}
elseif(!empty($_GET['mvid']))
{
    echo get_url_mv($_GET['mvid']);
}
else
{
    echo 'nothing';
}
?>