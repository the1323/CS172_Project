const express = require("express");
const bodyParser = require("body-parser");
const cors = require("cors");
const bookData = require("./book");
const app = express();
const port = 3000;

let books = bookData.books;
//console.log(bookData.books);
app.use(cors());

app.use(express.urlencoded({ extended: false }));
//app.use(bodyParser.urlendoded());
app.use(bodyParser.json());
app.post("/book", (req, res) => {
  //dddddd
  const book = req.body;
  console.log(book);
  books.push(book);
  res.send("book is added to db ");
});

app.get("/books", (req, res) => {
  res.json(books);
});

app.post("/book/:isbn", (req, res) => {
  const isbn = req.params.isbn;
  const newBook = req.body;
  console.log("asdasdasdasdasdasd");
  console.log(newBook);

  for (let i = 0; i < books.length; i++) {
    if (books[i].isbn === isbn) {
      console.log("/book/:isbn fff");
      console.log(books[i]);
      books[i] = newBook;
    }
  }
  res.send("book is edited");
});
app.get("/book/:isbn", (req, res) => {
  const isbn = req.params.isbn;

  for (let i = 0; i < books.length; i++) {
    if (books[i].isbn === isbn) {
      let current = books[i];
      res.send(current);
    }
  }
});
app.delete("/book/:isbn", (req, res) => {
  const isbn = req.params.isbn;

  for (let i = 0; i < books.length; i++) {
    if (books[i].isbn === isbn) {
      books.splice(i, 1);
    }
  }
  res.send("DELETE Request Called");
});

app.listen(port, () => console.log("hellooooooo"));
