<?php
global $lang;
$lang = "fr";
$string = file_get_contents("../../poems/poems.json");
$p = json_decode($string);

include($_SERVER['DOCUMENT_ROOT']."/content/poetry.php");
?>
