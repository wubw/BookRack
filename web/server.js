var express = require("express");
const MongoClient = require("mongodb").MongoClient;
const assert = require("assert");

// Connection URL
const url = "mongodb://localhost:27017";

// Database Name
const dbName = "books";

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

app.get("/books", function (req, res) {
  // Use connect method to connect to the Server
  // Create a new MongoClient
  const client = new MongoClient(url, {
    useNewUrlParser: true,
    useUnifiedTopology: true,
  });
  client.connect(function (err) {
    assert.equal(null, err);
    const db = client.db(dbName);
    db.collection("douban")
      .find({ reading_status: req.query.reading_status })
      .project({
        title: 1,
        rating: 1,
        ratingpeople: 1,
        my_rating: 1,
        _id: 1,
        info: 1,
        img: 1,
        timestamp: 1,
        douban_url: 1,
      })
      .toArray(function (err, result) {
        if (err) throw err;

        result.forEach(function (elem) {
          if (elem.ratingpeople === undefined) {
            elem.ratingpeople = "";
          }
          if (elem.my_rating === undefined) {
            elem.my_rating = "";
          }
          if (elem.info) {
            let splits = elem.info.split("||");
            console.log(splits);
          }
        });

        res.write(JSON.stringify(result));
        res.end();
        client.close();
      });
  });
});
