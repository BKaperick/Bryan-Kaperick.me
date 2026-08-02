<?php
global $lang;
$lang = "en";
$string = file_get_contents("../../blog/posts.json");
$p = json_decode($string);

include($_SERVER['DOCUMENT_ROOT']."/blog-posts.php");
?>