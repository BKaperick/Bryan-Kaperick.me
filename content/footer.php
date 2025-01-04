<footer class="footer layout__footer">
<span style="color:grey"> 
<p><span>© <?php echo $language['SITE_TITLE'] ?></span> – <nobr><?php echo $language['Site last updated'] ?>  <?php include($_SERVER['DOCUMENT_ROOT']."/widgets/last_update_date.txt"); ?></nobr>
<br>
<?php echo $language['SKETCH_CRED'] ?> <a href="https://www.instagram.com/j.andrews96/" style="color:#585858">Jason Andrews</a>
<br>
<a href="<?="/" . $lang . "/attributions/attributions.php"?>" style="color:grey"><?php echo $language['Click for other artistic attributions'] ?></a>
</p>
</span>
<button id="toggle">Toggle Dark Mode</button>


<script>
const root = document.documentElement;
const toggle = document.getElementById("toggle");
const darkMode = localStorage.getItem("dark-mode");
if (darkMode) {
  root.classList.add("dark-theme");
}
toggle.addEventListener("click", () => {
  root.classList.toggle("dark-theme");
  if (root.classList.contains("dark-theme")) {
    localStorage.setItem("dark-mode", true);
  } else {
    localStorage.removeItem("dark-mode");
  }
});
</script>
</footer>
