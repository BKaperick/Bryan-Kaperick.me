# Subdirectory structure

`photos.json` contains one object per photo, and the associated metadata.

# Usage

When a new photo is added, the following steps are necessary:
1. Create `./new/photo_name.jpg` containing the photo.
2. `python instantiate.py` moves the photo to `./raw/` and creates an entry in `photos.json`
3. Manually inspect the new entry in `photos.json` and fix any metadata details that are incorrectly filled.
4. `python create_html.py > photos.html` adds the new entry to the html read by `../$lang/photos/photos.html

# TODO
Automate steps 2 and 4.
