import os
import pymongo
from difflib import SequenceMatcher

mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["books"]
mongo_col = mongo_db["douban"]

book_rootpath = "/Users/wubinwei/WarmData/01 Books"
file_match = 0
file_nomatch = 0


def search_book_fromdb(name):
    find_book = mongo_col.find_one({"title": name})
    if find_book != None:
        return True

    find_book = mongo_col.find_one({"title": {'$regex': name}})
    if find_book != None:
        similarity = SequenceMatcher(
            None, name, find_book['title']).ratio()
        if similarity > 0.6:
            return True


for root, dirs, files in os.walk(book_rootpath, topdown=False):
    for f in files:
        # print(os.path.join(root, f))
        # print(f)
        if f == '.DS_Store':
            continue

        if root[-4] == '-':
            continue

        splits = os.path.splitext(f)
        fname = splits[0]
        ext = splits[1]
        if len(fname) > 4 and fname[-4] == '-':
            fname = fname[:-4]

        res = search_book_fromdb(fname)
        if res:
            file_match = file_match + 1
            continue

        print(os.path.join(root, f))
        file_nomatch = file_nomatch + 1

    for d in dirs:
        if len(d) < 4 or d[-4] != '-':
            continue
        dname = d[:-4]
        res = search_book_fromdb(dname)
        if res:
            file_match = file_match + 1
            continue

        print(os.path.join(root, d))
        file_nomatch = file_nomatch + 1

print(file_match)
print(file_nomatch)
