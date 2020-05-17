var express = require("express");
const MongoClient = require("mongodb").MongoClient;
const assert = require("assert");

// Connection URL
const url = "mongodb://localhost:27017";

// Database Name
const dbName = "books";

// Create a new MongoClient
const client = new MongoClient(url, {
  useNewUrlParser: true,
  useUnifiedTopology: true,
});

// Use connect method to connect to the Server
client.connect(function (err) {
  assert.equal(null, err);
  console.log("Connected successfully to server");

  const db = client.db(dbName);
  db.collection("douban")
    .find({ reading_status: "reading" })
    .project({ title: 1, _id: 0 })
    .toArray(function (err, result) {
      if (err) throw err;
      console.log(result);
      client.close();
    });
});

var app = express();
app.use(express.static("public"));
app.use(express.json({ limit: "50mb" }));
app.use(express.urlencoded({ limit: "50mb" }));

app.get("/", function (req, res) {
  res.sendFile("public/main.html", { root: __dirname });
});

var port = process.env.PORT || 3001;
var server = app.listen(port);
console.log("Express app started on port " + port);

app.get("/books", function (req, res) {});
