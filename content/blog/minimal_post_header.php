<?php 
$string = file_get_contents($_SERVER['DOCUMENT_ROOT']."/blog/posts.json");
$p = json_decode($string);
global $p;
?>
