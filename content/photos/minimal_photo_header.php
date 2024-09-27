<?php
$string = file_get_contents($_SERVER['DOCUMENT_ROOT']."/photos/photos.json");
$p = json_decode($string);
global $p;
?>
