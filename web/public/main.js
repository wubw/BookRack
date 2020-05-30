booklist = [];
tagfilter = [];
filteredbooklist = [];

Array.prototype.remove = function () {
  var what,
    a = arguments,
    L = a.length,
    ax;
  while (L && this.length) {
    what = a[--L];
    while ((ax = this.indexOf(what)) !== -1) {
      this.splice(ax, 1);
    }
  }
  return this;
};

function renderpage(reading_status) {
  $.get(
    "http://localhost:3001/books",
    { reading_status: reading_status },
    function (data) {
      booklist = JSON.parse(data);
      tagfilter = [];
      renderbooktable();
      rendersummary();
    }
  );
}

function renderbooktable() {
  let booklisttb = $("#booklisttb");
  booklisttb
    .empty()
    .append(
      '<caption>Douban Books</caption><tr><th align="left">Title</th><th align="left">Author</th><th align="left">Rating</th><th align="left">Rating People</th><th align="left">My Rating</th></tr>'
    );
  filteredbooklist = [];
  booklist.forEach(function (book) {
    let filtered = false;
    if (book.tags) {
      t = [];
      book.tags.split(" ").forEach(function (tag) {
        if (tag === "标签:") return;
        t.push(tag);
      });
      tagfilter.forEach(function (tf) {
        if (!t.includes(tf)) {
          filtered = true;
        }
      });
    } else {
      if (tagfilter.length !== 0) {
        filtered = true;
      }
    }
    if (filtered) {
      return;
    }
    filteredbooklist.push(book);
    booklisttb.append(
      "<tr><td>" +
        '<a href="http://localhost:3001/book.html?id=' +
        book._id +
        '" target="_blank">' +
        book.title +
        "</a>" +
        "</td><td>" +
        book.author +
        "</td><td>" +
        book.rating +
        "</td><td>" +
        book.ratingpeople +
        "</td><td>" +
        book.my_rating +
        "</td></tr>"
    );
  });
}

function rendersummary() {
  let tags = {};
  booklist.forEach(function (book) {
    if (book.tags) {
      book.tags.split(" ").forEach(function (tag) {
        if (tag === "标签:") return;
        if (tag in tags) {
          tags[tag]++;
        } else {
          tags[tag] = 1;
        }
      });
    }
  });

  let booksummarydiv = $("#booksummarydiv");
  booksummarydiv.empty();
  booksummarydiv.append(
    "<i>Books count: " + booklist.length + "</i><br/><br/>"
  );
  booksummarydiv.append(
    "<i id='filteredbookcount'>Filtered books count: " +
      filteredbooklist.length +
      "</i><br/><br/>"
  );
  let cnt = 0;
  Object.keys(tags).forEach(function (k) {
    booksummarydiv.append(
      '<a id="button" title="button">' + k + " " + tags[k] + "</a>"
    );
    cnt++;
    if (cnt === 3) {
      cnt = 0;
      booksummarydiv.append("<br/>");
    }
  });
  $(document).ready(function () {
    $("a#button").click(function () {
      $(this).toggleClass("down");
      let splits = $(this).text().split(" ");
      let key = splits[0];
      if (tagfilter.includes(key)) {
        tagfilter.remove(key);
      } else {
        tagfilter.push(key);
      }
      console.log(tagfilter);
      renderbooktable();
      let filteredbookcount = $("#filteredbookcount");
      filteredbookcount.text(
        "Filtered books count: " + filteredbooklist.length
      );
    });
  });
}

$("#booklisttb").ready(function () {
  renderpage("reading");
});

$("input[type=radio][name=doubanbook_readingstatus]").change(function () {
  renderpage(this.value);
});
