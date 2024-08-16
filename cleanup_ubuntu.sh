cd public

# index.html is a special case since it can't be in a language-specific 
# directory, so we have the default one (english) and the alternate (french) one
# in ./public/ named `index_fr.html`.  A bit ugly, but it works.
mv 'index.html?lang=fr.html' index_fr.html
cd content/fr

# Create canonical french-language files
find . -type f -exec rename 's/\?lang=fr//' {} +
cd ../..

# Remove excess files
find . -type f -name '*\?*' -delete
find . -type f -name '*.orig' -delete

# Change all urls from using ?lang= php vars to the proper `/en/` or `/fr/` subdirectory.
find . -type f -wholename "./content/*" -exec sed -i -E "s/href=\"(.*).php%3Flang=(\w\w)/href=\"\/content\/\2\/\1\/\1.php/g" {} \;
#find . -type f -wholename "./content/*" -exec sed -i -E "s/href=\"(.*).php%3Flang=(\w\w)/href=\".\/\1.php/g" {} \;

find . -type f -name "index_fr.html" -exec sed -i -E "s/index.html%3Flang=en.html/index.html/g" {} \;
find . -type f -name "index.html" -exec sed -i -E "s/index.html%3Flang=fr.html/index_fr.html/g" {} \;

# All links on french pages back to index.html need to point to index_fr.html instead.
find . -type f -wholename "./content/fr/*" -exec sed -i -E "s/index.html/index_fr.html/g" {} \;
# All links to `index.html` in `index_fr.html` except the language toggle need to point to `index_fr.html`
find . -type f -name "index_fr.html" -exec sed -i -E 's/<a href="index.html" title="Home"/<a href="index_fr.html" title="Home"/g' {} \;

# At the end, rename everything to use `.html` rather than the uglier `.html`. 
find . -type f -exec rename 's/.html/.html/' {} +
find . -type f -wholename "*" -exec sed -i -E "s/.html/.html/g" {} \;

# HACK TODO fix blog post urls, `header.php` creates language toggle but doesnt have access to current path
# find . -type f -wholename "./content/fr/blog-post/(?!blog-post.html)" -exec sed -i -E "s/\/content\/(\w\w)\/(.*)\/(.*).html/\/content\/\1\/blog-post\/\3.html/g" {} \;
find . -type f -wholename "./content/*/blog-post/*" -exec sed -i -E "s/\/content\/(\w\w)\/(.*)\/(.*).html/\/content\/\1\/blog-post\/\3.html/g" {} \;
