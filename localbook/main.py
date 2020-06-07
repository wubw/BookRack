import localbook_search

douban_books = localbook_search.retrieve_allbooks_fromdb()
book_rootpath = "/Users/wubinwei/WarmData/01 Books"
file_match, file_nomatch = localbook_search.search_book_fromlocal(
    book_rootpath, douban_books)
print(file_match)
print(file_nomatch)
