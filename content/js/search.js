
function populate_result_suggestions(results) {
  
  var suggestions = document.getElementById("partial_search_results");
  // Erase previous suggestions
  suggestions.innerHTML = ''
  results.forEach((i,result_ind) => {
    console.log(result_ind);
    var poem_block = document.getElementById(i);
    console.log("Found: " + i);
    var option = document.createElement("option")
    option.value = i
    option.innerHTML = i;
                
    suggestions.appendChild(option);
  })
};

function redirect_from_results(results) {
  const user_query = document.getElementById('search_query').value;

  console.log("query submitted");
  console.log(user_query);
  
  
  results.forEach((i,result_ind) => {
    console.log(result_ind);
    var poem_block = document.getElementById(i);
    console.log("Found: " + i);

  if (result_ind == 0) {
    
    console.log("Redirecting to: " + poem_block.parentNode);
    window.location.href= poem_block.parentNode; 
    };
  })
};