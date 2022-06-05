
/**
 * main main function, fetch search result
 */
 function getResults(){
    let searchQuery = document.getElementById("searchBar").value
    console.log(searchQuery);


 }

 function renderResults(){
   const r = document.getElementById("results")
    for (let i = 0;i<10;i++){
      //title,body,url = findData()
      var page = document.createElement('li');
      var title = document.createElement('a');
      title.innerHTML = "sometitle" + i;
      title.href = "https://www.youtube.com/watch?v=e1KJ47tyCso"
      var snippet = document.createElement('p');
      snippet.innerHTML = "Command-line interface is one of the preferred ways for nerds like us to get stuff done. People who are better at using keyboard then mouse. In this video we will learn ho";
      page.appendChild(title);
      page.appendChild(snippet);
      r.appendChild(page)
    }

    
 }
 renderResults()