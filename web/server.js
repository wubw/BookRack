var express = require("express");
const MongoClient = require("mongodb").MongoClient;
const ObjectID = require("mongodb").ObjectID;
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

function parse_info_data(info_data) {
  let splits = info_data.split("||");
  const searchkeywords = {
    "作者:": "author",
    "出版社:": "publisher",
    "副标题:": "sub-title",
    "出版年:": "publish-time",
    "页数:": "pages",
    "译者:": "translator",
    "原作名:": "original-title",
    "定价:": "",
    "装帧:": "",
    "丛书:": "",
    "ISBN:": "",
  };
  let tempBuf = [];
  let searchkey = "";
  let results = {};
  splits.forEach(function (elem) {
    if (elem in searchkeywords) {
      if (searchkey) {
        results[searchkey] = tempBuf.join(" ");
      }
      tempBuf = [];
      searchkey = searchkeywords[elem];
      return;
    }
    if (searchkey) {
      tempBuf.push(elem);
    }
  });
  return results;
}

app.get("/books", function (req, res) {
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
        tags: 1,
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
            info_data = parse_info_data(elem.info);
            Object.assign(elem, info_data);
          }
        });
        res.write(JSON.stringify(result));
        res.end();
        client.close();
      });
  });
});

app.get("/book", function (req, res) {
  const client = new MongoClient(url, {
    useNewUrlParser: true,
    useUnifiedTopology: true,
  });
  client.connect(function (err) {
    assert.equal(null, err);
    const db = client.db(dbName);
    db.collection("douban").findOne({ _id: ObjectID(req.query.id) }, function (
      err,
      result
    ) {
      if (err) throw err;
      if (result.info) {
        info_data = parse_info_data(result.info);
        Object.assign(result, info_data);
      }
      res.write(JSON.stringify(result));
      res.end();
      client.close();
    });
  });
});

app.get("/localbooks", function (req, res) {
  const client = new MongoClient(url, {
    useNewUrlParser: true,
    useUnifiedTopology: true,
  });
  client.connect(function (err) {
    assert.equal(null, err);
    const db = client.db(dbName);
    db.collection("match")
      .find({})
      .toArray(function (err, result) {
        if (err) throw err;
        res.write(JSON.stringify(result));
        res.end();
        client.close();
      });
  });
});

app.get("/localbook", function (req, res) {
  const client = new MongoClient(url, {
    useNewUrlParser: true,
    useUnifiedTopology: true,
  });
  client.connect(function (err) {
    assert.equal(null, err);
    const db = client.db(dbName);
    db.collection("match").findOne(
      { douban_url: req.query.douban_url },
      function (err, result) {
        if (err) throw err;
        if (!result) result = {};
        res.write(JSON.stringify(result));
        res.end();
        client.close();
      }
    );
  });
});
