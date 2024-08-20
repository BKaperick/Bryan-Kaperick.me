<?php
    global $language;
    $lang = $_GET["lang"] ?? "en";
    require_once("./view/Language/lang.".$lang.".php");
    include $_SERVER['DOCUMENT_ROOT'] . '/mainpage.php';
?>
<style>
  <?php include $_SERVER['DOCUMENT_ROOT'] . "/style.css" ?>
</style>
