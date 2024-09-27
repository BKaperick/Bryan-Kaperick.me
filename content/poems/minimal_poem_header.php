<?php 
$string = file_get_contents($_SERVER['DOCUMENT_ROOT']."/poems/poems.json");
$p = json_decode($string);
global $p;
?>
