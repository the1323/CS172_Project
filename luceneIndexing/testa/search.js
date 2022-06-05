
/**
 * main main function, fetch search result
 */
let isLoaded = false;
function handleSearch(){
  isLoaded = false
    let searchQuery = document.getElementById("searchBar").value
    console.log("func handleSearch")
    let body = {
      query: searchQuery
    };
    
    const response = fetch('http://localhost:3000/create', {
      method: 'post',
      body: JSON.stringify(body),
      headers: {'Content-Type': 'application/json'}
  });
  
  console.log("response " + response.text)
  var myRes = response.text;
  
  
  
}

function getResults() {
    let searchQuery = document.getElementById("searchBar").value
    console.log(searchQuery);

    // parseCsv()
    // renderResults()


}




async function loadBooks() {
    let response = await fetch("http://localhost:3000/create");
    console.log(response.status);
    console.log(response.statusText);
  
    if (response.status === 200) {
      let result = await response.text();
      

      let re = JSON.parse(result);
      console.log(re[0])
      if(re.length > 0 ) isLoaded = true;
      const r = document.getElementById("results");
      while (r.firstChild) {
        r.firstChild.remove()
    }
      for (let i = 0; i < re.length; i++) {
        //title,body,url = findData()
        var page = document.createElement('li');
        var title = document.createElement('a');
        
        title.innerHTML = re[i].title;
        var score = document.createElement('p');
        score.innerHTML = re[i].score;
        title.href = re[i].url
        var snippet = document.createElement('p');
        snippet.innerHTML = re[i].snippet;
        
        page.appendChild(title);
        page.appendChild(score)
        page.appendChild(snippet);
        page.className = "list-group-item";
        r.appendChild(page)
    }
    }
  
    
}
var intervalId = setInterval(function() {
  if(! isLoaded)
  loadBooks()
}, 1000);

