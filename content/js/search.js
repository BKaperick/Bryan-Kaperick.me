function run_search_query(index, user_query) {
  return index.search(user_query, { suggest: false });
}

function listen_on_input(listen) {
  var form = document.getElementById("searchForm");
  form.addEventListener('input', event => {
    event.preventDefault(); 
    listen();
  });
}

function populate_result_suggestions(titles, results) {
  
  var suggestions = document.getElementById("partial_search_results");
  // Erase previous suggestions
  suggestions.innerHTML = ''
  console.log("Query returned " + results.length + " results:")
  results.forEach((i,result_ind) => {
    var poem_block = document.getElementById(i);
    var option = document.createElement("option")
    option.value = titles[i]; // to make auto-complete
    //option.innerHTML = titles[i]; // for display
                
    suggestions.appendChild(option);
  })
};

function hide_nonmatching_results(keys, results) {
  keys.forEach(key => {
    var poem_block = document.getElementById(key);
    if (results.indexOf(key) == -1) {
      poem_block.style.display = 'none';
    } else {
      poem_block.style.display = 'block';
    }

  })
};

function highlight_matching_text(input, class_name) {
  const mark_regex = /<mark>(.*)<\/mark>/;
  // It needs a capturing group in order to replace while respecting capitalization
  const input_regex = new RegExp("(" + input + ")", "i");
  [...document.getElementsByClassName(class_name)].forEach(line => {

      // Remove existing mark
      line.innerHTML = line.innerHTML.replace(mark_regex, "$1");
      // Add new one
      line.innerHTML = line.innerHTML.replace(input_regex, "<mark>$1</mark>");
  });
};

function redirect_from_results(results) {
  const user_query = document.getElementById('search_query').value;

  console.log("query submitted");
  console.log(user_query);
  
  
  results.forEach((i,result_ind) => {
    var poem_block = document.getElementById(i);
    // console.log("Found: " + i);

  if (result_ind == 0) {
    
    console.log("Redirecting to: " + poem_block.parentNode);
    window.location.href= poem_block.parentNode; 
    };
  })
};