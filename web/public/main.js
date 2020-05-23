function renderbooktable(reading_status) {
  $.get(
    "http://localhost:3001/books",
    { reading_status: reading_status },
    function (data) {
      let booklisttb = $("#booklisttb");
      booklisttb
        .empty()
        .append(
          '<caption>Douban Books</caption><tr><th align="left">Title</th><th align="left">Rating</th><th align="left">Rating People</th><th align="left">My Rating</th></tr>'
        );
      let booklist = JSON.parse(data);
      booklist.forEach(function (book) {
        booklisttb.append(
          "<tr><td>" +
            book.title +
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
  );
}

$("#booklisttb").ready(function () {
  renderbooktable("reading");
});

$("input[type=radio][name=doubanbook_readingstatus]").change(function () {
  renderbooktable(this.value);
});
