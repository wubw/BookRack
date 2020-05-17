import os
import pymongo
import json
import base64
from pathlib import Path

data_dir = '../data'
downloaded_filename = '../data/downloaded.txt'

mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["books"]
mongo_col = mongo_db["douban"]

collist = mongo_db.list_collection_names()
print(collist)

downloaded_books = []
if os.path.isfile(downloaded_filename):
    downloaded_file = open(downloaded_filename, 'r')
    downloaded_books = downloaded_file.read().splitlines()
    downloaded_file.close()

# print(downloaded_books)
# print(len(downloaded_books))

downloaded_books = list(dict.fromkeys(downloaded_books))

# print(len(downloaded_books))

bookdatacnt = 0
books = []
for root, dirs, files in os.walk(data_dir, topdown=False):
    for name in files:
        if name == "book":
            bookdatacnt = bookdatacnt + 1
            downloaded_file = open(os.path.join(root, name), 'r')

            content = eval(downloaded_file.read())
            stat = os.stat(os.path.join(root, name))
            content['file_create_time'] = stat.st_birthtime

            imgfile = os.path.join(root, 'cover.jpg')
            if Path(imgfile).is_file():
                with open(imgfile, mode='rb') as file:
                    img_data = file.read()
                    content['img_data'] = base64.encodebytes(
                        img_data).decode("utf-8")

            books.append(content)
        #print(os.path.join(root, name))
    # for name in dirs:
    #    print(os.path.join(root, name))


def sort_books_func(e):
    return e['file_create_time']


books.sort(key=sort_books_func)

# print(bookdatacnt)

# fix = {'https://book.douban.com/subject/1025643/': '全球通史',
#        'https://book.douban.com/subject/1674929/': '材料力学'}

j = 0
for i in range(len(downloaded_books)):
    # if downloaded_books[i] in fix:
    #     print(downloaded_books[i] + ' =====> ' + fix[downloaded_books[i]])
    #     continue

    print(downloaded_books[i] + ' =====> ' + books[j]['title'])
    books[j]['douban_url'] = downloaded_books[i]
    # print(json.dumps(books[j]))

    mongo_col.insert_one(books[j])
    j = j+1

books_reading_status = {'will_read': [], 'reading': [], 'have_read': []}
for book in books:
    books_reading_status[book['reading_status']].append(book)

# print(len(books_reading_status['reading']))
# print(len(books_reading_status['have_read'])+2)
# print(len(books_reading_status['will_read']))
