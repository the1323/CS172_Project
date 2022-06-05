async function loadBooks() {
  let response = await fetch("http://localhost:3000/books");
  console.log(response.status);
  console.log(response.statusText);

  if (response.status === 200) {
    let data = await response.text();
    //console.log(data);
    const books = JSON.parse(data);
    for (let book of books) {
      const x = `
      <div class="col-4">
            <div class="card">
                <div class = "card-body">
                <h5 class="card-title">${book.title}</h5>
                <h6 class="card-subtitle mb-2 text-muted">${book.isbn}</h6>
                    <div>Author: ${book.author}</div>
                    <div>Publisher: ${book.publisher}</div>
                    <div>Number of Pages: ${book.pages}</div>
                    <div>Published Date: ${book.publish_date}</div>
                    <hr>

                    <button type = "button" class = "btn btn-danger" onClick="deleteBook(${book.isbn})">Delete</button>
                    <button type = "button" class = "btn btn-primary" data-toggle="modal" 
                        data-target="#editBookModal" onClick="setEditModal(${book.isbn})">
                        Edit
                    </button>
                </div>
            </div>
        </div>
        `;
      document.getElementById("books").innerHTML =
        document.getElementById("books").innerHTML + x;
    }
  }
}

async function setEditModal(isbn) {
  let response = await fetch(`http://localhost:3000/book/${isbn}`);

  console.log(response.status);
  console.log(response.statusText);

  if (response.status === 200) {
    let data = await response.text();

    console.log("dataaaaaaaaa");
    const book = JSON.parse(data);

    document.getElementById("isbn").value = book.isbn;
    document.getElementById("title").value = book.title;
    document.getElementById("author").value = book.author;
    document.getElementById("publish_date").value = book.publish_date;
    document.getElementById("publisher").value = book.publisher;
    document.getElementById("numOfPages").value = book.pages;

    document.getElementById(
      "editForm"
    ).action = `http://localhost:3000/book/${isbn}`;
  }
}

async function deleteBook(isbn) {
  let response = await fetch(`http://localhost:3000/book/${isbn}`, {
    method: "DELETE",
  });

  console.log(response.status);
  location.reload();
}
function JsExecCmd(value) {

  var shell = WScript.CreateObject("WScript.Shell");
  shell.Run("command here");
  
  /*
  
  命令参数说明
  
  cmd.exe /c dir 是执行完dir命令后关闭命令窗口。
  
  cmd.exe /k dir 是执行完dir命令后不关闭命令窗口。
  
  cmd.exe /c start dir 会打开一个新窗口后执行dir指令，原窗口会关闭。
  
  cmd.exe /k start dir 会打开一个新窗口后执行dir指令，原窗口不会关闭。
  
  */
  
  
  //执行完cmd命令后不关闭命令窗口。
  
  // cmd.run("cmd.exe /k "+value);
  
  
  
  // //执行完cmd命令后不关闭命令窗口。
  
  // cmd.run("cmd.exe /k "+value);
  
  
  
  // cmd = null;
  
  }

  
   
  
  function run() {
  
  var command = "echo lance  shuai  i love  !" //这里是执行的DOS命令
  
  JsExecCmd(command );
  
  }


loadBooks();
