
function run_search_query(index, user_query) {
  return index.search(user_query, { suggest: false });
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
}

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