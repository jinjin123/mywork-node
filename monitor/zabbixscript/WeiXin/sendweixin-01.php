<?php
require "config-01.php";
require "include/WeiXin.php";
$weixin = new WeiXin($G_CONFIG['weiXin']);
$user = "$argv[1]";
$dep = "$argv[2]";
$tag = "$argv[3]";
$msg = "$argv[4]";
$result = $weixin->send("$user", "$dep", "$tag", "$msg");
print_r($result);
?>
