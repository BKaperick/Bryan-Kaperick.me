<?php 
$lang = $_GET["lang"] ?? "en";
global $language;

include($_SERVER['DOCUMENT_ROOT']."/header.php");
include($_SERVER['DOCUMENT_ROOT']."/".$lang."/blog-post/beatnik.html");
include($_SERVER['DOCUMENT_ROOT']."/footer.php");
?>
