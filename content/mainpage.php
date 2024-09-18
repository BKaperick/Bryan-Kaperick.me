<?php 
$lang = $_GET["lang"] ?? "en";
include($_SERVER['DOCUMENT_ROOT']."/header.php");
include($_SERVER['DOCUMENT_ROOT']."/".$lang."/mainpage.html");
include($_SERVER['DOCUMENT_ROOT']."/footer.php");
?>
