<?php
$lang = $_GET["lang"] ?? "en";
global $language;
require_once($_SERVER['DOCUMENT_ROOT']."/view/Language/lang.".$lang.".php");

$string = file_get_contents($_SERVER['DOCUMENT_ROOT']."/content/now/now.json");
$p = json_decode($string);

include($_SERVER['DOCUMENT_ROOT']."/content/header.php");
include($_SERVER['DOCUMENT_ROOT']."/content/".$lang."/now/now.html");
include($_SERVER['DOCUMENT_ROOT']."/content/footer.php");
?>