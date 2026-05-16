function photos_input_listen(index) {
  const photo_block_ids = [...document.getElementsByClassName('main-page-photo-block')]
    .map(element => element.id);

  const user_query = document.getElementById('search_query').value;
  if (user_query == "") {
    var res = photo_block_ids;
  }
  else {
    var res = run_search_query(index, user_query);
  }

  hide_nonmatching_results(photo_block_ids, res);
  highlight_matching_text(user_query,  "photo-caption");
}

function load_photos_index(index, language) {
  fetch("../../photos/photos.json")
  .then(response => response.json())
  .then(data => 
  {
      key_to_album_key = get_photo_keys_to_album_keys(data);
      for (let [key, value] of Object.entries(data))
      {
        var data = value["year"];
        if ("people" in value)
          data += " " + value["people"].join(" ");
        if (language in value)
          data += " " + value[language];
        if (key in key_to_album_key)
          key_to_index = key_to_album_key[key];
        else
          key_to_index = key;
        index.append(key_to_index, data);
      };
  });
}

function get_photo_keys_to_album_keys(photos, key) {
  key_to_album_key = {}
  for (let [key, value] of Object.entries(photos)) {
    if ("photos" in value) {
      for (let sub_key of Object.values(value["photos"])) {
        key_to_album_key[sub_key] = key;
      }
    }
  }
  return key_to_album_key;
}