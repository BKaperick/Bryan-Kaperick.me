<?php 
$lang = $_GET["lang"] ?? "en";
global $language;
require_once($_SERVER['DOCUMENT_ROOT']."/view/Language/lang.".$lang.".php");

$string = file_get_contents($_SERVER['DOCUMENT_ROOT']."/bio/books.json");
$p = json_decode($string);

include($_SERVER['DOCUMENT_ROOT']."/header.php");
include($_SERVER['DOCUMENT_ROOT']."/".$lang."/bio/bio.html");
include($_SERVER['DOCUMENT_ROOT']."/footer.php");
?>
