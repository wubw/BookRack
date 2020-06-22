const urlParams = new URLSearchParams(window.location.search);
const book_id = urlParams.get("id");

$.get("http://localhost:3001/book", { id: book_id }, function (data) {
  book = JSON.parse(data);
  $("#title").text(book.title);
  $("#author").text(book.author);
  $("#publisher").text(book.publisher);
  $("#sub-title").text(book["sub-title"]);
  $("#publish-time").text(book["publish-time"]);
  $("#pages").text(book.pages);
  $("#translator").text(book.translator);
  $("#original-title").text(book["original-title"]);
  $("#douban_url").text(book["douban_url"]).attr("href", book["douban_url"]);

  $.get(
    "http://localhost:3001/localbook",
    { douban_url: book["douban_url"] },
    function (d) {
      lbd = JSON.parse(d);
      if ("local_path" in lbd) {
        $("#localpath").text(lbd.local_path);
        $("#similarity").text(lbd.similarity);
      }
    }
  );

  let tagsdiv = $("#tags");
  if (book.tags) {
    book.tags.split(" ").forEach(function (tag) {
      if (tag === "标签:") return;
      tagsdiv.append("<i>" + tag + "</i>");
    });
  }

  $("#img").attr("src", "data:image/jpg;base64," + book.img_data);
});
