# Subdirectory structure

`poems.json` contains the poems and associated metadata.  This is what gets ingested to create php/html with `create_html.py` but is not read directly when loading the page.

`./new/` stores new poems in plain-text.  The name of each file is the title with underscores instead of spaces, and no special characters or capitalization.

`./raw/` is where plain-text poems are moved once they have been instantiated by instantiate.py.  This is the permanent location of the source-truth poem and they should never be edited.

`instantiate.py` follows the json schema to create a new object in `poems.json` with some basic metadata and a guess for its name.  One must manually update `poems.json` to fix the metadata (add back any special characters in the title, for example).

`format_poem.py` reads from `./raw/` directory and prepares the html body of the poem by handling special characters and spacing.
    Usage:
    `python format_poem.py` - adds body to any poems in `poems.json` that don't have an existing `body` key.
    `python format_poem.py all-poems` - overwrites body key-value for every poem containing a `rawpath` key (otherwise we have nothing to write).
    `python format_poem.py [poems]` - pass an explicit space-separated list of poem keys to overwrite in addition to any missing a `body` key.

`create_html.py` reads `poems.json` and creates the php/html blocks needed to embed them in a page in reverse-chronological order.

# Usage

When a new poem is added, the following steps are necessary.
1. Create `./new/poem_name.txt` containing plain-text of poem.
2. `python instantiate.py`
3. `python format_poem.py`
4. Manually inspect the new entry in `poems.json` and fix any metadata details that are incorrectly filled.
5. `python create_html.py` to generate `poems_inspiration.html`, `poems2024.html`, `poems2023.html`, and `poems2022.html` to be read by `/$lang/poetry/poetry.html`.

# TODO
We want to automate steps 2, 3, and 5 above.
