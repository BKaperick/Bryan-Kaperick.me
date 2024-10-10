<?php 
$lang = "en";
global $language;
require_once($_SERVER['DOCUMENT_ROOT']."/view/Language/lang.".$lang.".php");

include($_SERVER['DOCUMENT_ROOT']."/header.php");
include($_SERVER['DOCUMENT_ROOT']."/".$lang."/projects/wiki-switcher.html");
include($_SERVER['DOCUMENT_ROOT']."/footer.php");
?>
