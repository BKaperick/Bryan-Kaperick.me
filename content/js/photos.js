
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
}

function load_photos_index(index) {
fetch("../../photos/photos.json")
.then(response => response.json())
.then(data => 
{
    for (let [key, value] of Object.entries(data))
    {
      if ("people" in value)
    index.add(key, value["people"].join(" ") + " " + value["en"]);
    };
});
}