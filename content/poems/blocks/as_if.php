<?php 
$lang = $_GET["lang"] ?? "en";
global $language;
require_once($_SERVER['DOCUMENT_ROOT']."/view/Language/lang.".$lang.".php");

$string = file_get_contents($_SERVER['DOCUMENT_ROOT']."/poems/poems.json");
$p = json_decode($string);
global $p;
include($_SERVER['DOCUMENT_ROOT']."/poems/./blocks/as_if.html");
?> 
