const express = require("express");
const bodyParser = require("body-parser");
const cors = require("cors");
const app = express();
const port = 3000;

var result = [];
var resultSize = -1;
var previous = " ";
var fo = "";
app.use(cors());

app.use(express.urlencoded({ extended: false }));

app.use(bodyParser.json());
app.post("/resultRowIndexer", (req, res) => {
  //dddddd
  const book = req.body;
  console.log(book);
  data.push(book);
  res.send("resultRowIndexer is added to db ");
});
async function getData(file) {
  
  const fs = require("fs");
  const csvParser = require("csv-parser");
  fs.createReadStream(file)
    .pipe(csvParser())
    .on("data", (data) => {
      console.log("result getting");
      result.push(data);
      //  console.log(result);
    })
    .on("end", () => {
      console.log("result done1 " + result.length);
      resultSize = result.length;
      console.log("result done2 " + resultSize);
    });
    
    
 // return result
}

app.post("/create", async (req, res) => {
  
  const query = req.body.query;
  if (query.length <1) return 
  if( query == previous && result.length !=0) {
    console.log("same " + result.length);
    res.send(result);
    return
  }
  previous = query;
  const fs = require('fs');
  console.log("query " + query);
  const file = '../queryCache/'+query+'.csv'
  fo = file
  var isExist = fs.existsSync(file);
  console.log("checkFileExist " + isExist);
  if (!isExist){
    const content = '';
    fs.writeFile(file, content, err => {
      if (err) {
        console.error(err);
      }
      // file written successfully
    });
  }

   
    
    result=[]
    await getData(file);
    
  
  console.log("hrer " + result.length + " " + resultSize);

  await res.send(result);
});

app.get("/create", async (req, res) => {
  //const query = req.body.query;
  //var data = "tta";
  //const book = req.body;
  //data = await getData();
  // console.log(data);
  if(fo.length>0)
  await getData(fo);
  res.send(result)
});



app.get("/resultRowIndexer", (req, res) => {

  const fs = require('fs');

  const content = 'Some content!';

  fs.writeFile('./test.txt', content, err => {
    if (err) {
      console.error(err);
    }
    // file written successfully
  });
  res.send(result);
});

app.listen(port, () => console.log("hellooooooo"));
