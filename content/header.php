<html>
<?php 
$lang = $_GET["lang"] ?? "en";
$language_toggle = array(
    'en'=>'fr', 
    'fr'=>'en');
?>

<link rel="stylesheet" href="/style.css">

<html lang="<?php echo $lang; ?>">
<html class="nojs" lang=$lang dir="ltr">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width">
<head>
<link rel="alternate" type="application/rss+xml" title="RSS" href="https://bryan-kaperick.me/index.xml">
<meta name="created" content="2021-10-24T18:44:04+0200">
<meta name="modified" content="2023-07-30T15:34:43+0200">


<meta property="og:site_name" content="Bryan Kaperick&#39;s Website">
<meta property="og:title" content="Welcome">
<meta property="og:url" content="https://bryan-kaperick.me/">
<meta property="og:type" content="website">

<meta name="msapplication-TileColor" content="#ffffff">
<meta name="theme-color" content="#ffffff">

<link rel="shortcut icon" type="image/x-icon" href="/static/favicon.ico">
<link rel="icon" type="image/x-icon" href="/static/favicon.ico">
<link rel="apple-touch-icon" href="/static/favicon.ico">



<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "WebPage",
    "url" : "https://bryan-kaperick.me/",
    "name": "Welcome",
    "mainEntityOfPage": {
      "@type": "WebPage",
      "@id": "https://bryan-kaperick.me/"
    },
    "publisher": {
      "@type": "Organization",
      "name": "Bryan Kaperick's Website",
      "url": "https://bryan-kaperick.me/"
    }
  }
</script>

</head>

<body class="list-page front">
<div class="page layout__page">
<header class="header layout__header">
<a href="/" title="Home" rel="home" class="header__logo"><img src="/static/logo_cleaned_reduce_50pct.webp" alt="Home" class="header__logo-image invertible"></a>
<h1 class="header__site-name">
<a href="/" title="Home" class="header__site-link" rel="home"><span><?php echo $language['SITE_TITLE'] ?></span></a>
</h1>
<div class="region header__region">
<h2 class="visually-hidden">Language selector</h2>
<nav class="language-selector layout__language-selector">

<a rel="alternate" lang="<?=$language_toggle[$lang]?>" hreflang="<?=$language_toggle[$lang]?>" href="?lang=<?=$language_toggle[$lang];?>"><div class="language_box"><div class="language_text language_text_<?=$lang?>"><?=$language['LANGUAGE_TOGGLE'];?></div>
<img src="/static/cafe-<?=$language_toggle[$lang]?>.webp" class="language_icon invertible"></div></a>
    

</nav>
</div>
</header>

<nav class="main-menu layout__navigation">
<h2 class="visually-hidden">Main menu</h2>
<ul class="navbar">
<li><a href="/"
<?=
(str_contains(basename($_SERVER['SCRIPT_FILENAME']), "index")) 
? "class=\"active\" aria-current=\"page\"" 
: "" ?>><?=$language['Home'];
?>
</a></li>
<li><a href="/<?=$lang?>/now/now.php"
<?=
(str_contains($_SERVER['SCRIPT_FILENAME'], "now")) 
? "class=\"active\" aria-current=\"page\"" 
: "" ?>><?=$language['Now'];
?>
</a></li>
<li><a href="/<?=$lang?>/poetry/poetry.php" 
<?=
(str_contains(basename($_SERVER['SCRIPT_FILENAME']), "poetry")) 
? "class=\"active\" aria-current=\"page\"" 
: "" ?>><?=$language['Poetry'];
?>
</a></li>
<li><a href="/<?=$lang?>/contact/contact.php"
<?=
(str_contains(basename($_SERVER['SCRIPT_FILENAME']), "contact")) 
? "class=\"active\" aria-current=\"page\"" 
: "" ?>><?=$language['Contact'];
?>
</a></li>
<li><a href="/<?=$lang?>/photos/photos.php"
<?=
(str_contains(basename($_SERVER['SCRIPT_FILENAME']), "photos")) 
? "class=\"active\" aria-current=\"page\"" 
: "" ?>><?=$language['Photos'];
?>
</a></li>
<li><a href="/<?=$lang?>/bio/bio.php"
<?=
(str_contains(basename($_SERVER['SCRIPT_FILENAME']), "bio")) 
? "class=\"active\" aria-current=\"page\"" 
: "" ?>><?=$language['Bio'];
?>
</a></li>
<li><a href="/<?=$lang?>/blog-post/blog-post.php"
<?=
(str_contains($_SERVER['SCRIPT_FILENAME'], "blog-post")) 
? "class=\"active\" aria-current=\"page\"" 
: "" ?>><?=$language['Blog Posts'];
?>
</a></li>
<li><a href="/<?=$lang?>/projects/projects.php"
<?=
(str_contains($_SERVER['SCRIPT_FILENAME'], "projects")) 
? "class=\"active\" aria-current=\"page\"" 
: "" ?>><?=$language['Projects'];
?>
</a></li>
</ul>

</nav>
