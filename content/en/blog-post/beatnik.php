<?php 
$lang = "en";
global $language;
require_once("../../../view/Language/lang.".$lang.".php");

include($_SERVER['DOCUMENT_ROOT']."/header.php");
include($_SERVER['DOCUMENT_ROOT']."/".$lang."/blog-post/beatnik.html");
include($_SERVER['DOCUMENT_ROOT']."/footer.php");
?>
