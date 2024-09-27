<?php 
$lang = $_GET["lang"] ?? "en";
global $language;
require_once($_SERVER['DOCUMENT_ROOT']."/view/Language/lang.".$lang.".php");

$string = file_get_contents($_SERVER['DOCUMENT_ROOT']."/photos/photos.json");
$p = json_decode($string);
global $p;
include($_SERVER['DOCUMENT_ROOT']."/minimal_header.html");
include($_SERVER['DOCUMENT_ROOT']."/photos/./raw_with_label/Swap_2022_1.html");
?> 
