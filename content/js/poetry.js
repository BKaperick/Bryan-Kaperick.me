
// Get all the headers, and inject the counts
function recount_visible_poems(max_do_unfold = 0) {
  const poem_count_regex = /(\d+) \(\d+/;
  [...document.getElementsByClassName('poem-year-details')].forEach(detail => {
    var poem_count = [...detail.getElementsByClassName('main-poem-page')]
      .filter(d => d.style.display != 'none').length;
    
    if (poem_count <= max_do_unfold) {
      detail.open = true;
    } else { detail.open = false;};
    [...detail.getElementsByClassName('poem-year-header')].forEach(header => {
      console.log(poem_count + ": " + header.innerHTML)
      header.innerHTML = header.innerHTML.replace(poem_count_regex, "$1 (" + poem_count);
    });
  });
};

function poetry_input_listen(index) {
  document.getElementById("my-works-det").open = true;
  const poem_block_ids = [...document.getElementsByClassName('main-poem-page')]
    .map(element => element.id);

  const user_query = document.getElementById('search_query').value;
  if (user_query == "") {
    var res = poem_block_ids;
    var max_fold = 0;
  }
  else {
    var res = run_search_query(index, user_query);
    var max_fold = 3;
  }

  hide_nonmatching_results(poem_block_ids, res);
  recount_visible_poems(max_fold); // Unfold if at most X poems in year match the query 

  // Highlight incremental matches in the content
  highlight_matching_text(user_query, "line");
  highlight_matching_text(user_query, "poem-title");
}

function load_poetry_index(index) {
fetch("../../poems/poems.json")
.then(response => response.json())
.then(data => 
{
    for (let [key, value] of Object.entries(data))
    {
    index.add(key, value["title"] + " " + value["raw_body"]);
    };
});
}