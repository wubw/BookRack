import os
import pymongo
from difflib import SequenceMatcher
from langconv import *


def retrieve_allbooks_fromdb():
    mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
    mongo_db = mongo_client["books"]
    mongo_col = mongo_db["douban"]

    douban_books = []
    for db in mongo_col.find():
        douban_books.append(db)
    return douban_books


t = 0.6


def remove_block(s: str, start, end):
    startidx = s.find(start)
    if startidx > 0:
        endidx = s.find(end)
        if endidx > 0:
            substr = s[startidx:endidx+1]
            s = s.replace(substr, '')
    return s


def process_string(s: str):
    s = remove_block(s, '[', ']')
    s = remove_block(s, '(', ')')
    s = remove_block(s, '《', '》')

    s = s.replace(' ', '')
    s = s.replace('_', '')
    s = s.replace('+', '')
    s = s.replace('-', '')
    s = s.replace('&', '')
    s = s.replace('%', '')

    return s.lower()


def process_string2(s: str):
    s = Converter('zh-hans').convert(s)
    return s


def compare_string(stra, strb):
    if stra == strb:
        return 1
    similarity = SequenceMatcher(None, process_string(
        stra), process_string(strb)).ratio()
    if similarity > t:
        print(similarity)
        return similarity

    similarity = SequenceMatcher(None, process_string2(
        stra), process_string2(strb)).ratio()
    if similarity > t:
        print(similarity)
    return similarity


def search_book_fromdb(name, douban_books):
    for db in douban_books:
        if compare_string(db['title'], name) > t:
            return db
        if 'sub-title' in db and compare_string(db['sub-title'], name) > t:
            return db
        if 'original-title' in db and compare_string(db['original-title'], name) > t:
            return db

    return None


def search_book_fromlocal(root_path, douban_books):
    file_match = 0
    file_nomatch = 0
    for root, dirs, files in os.walk(root_path, topdown=False):
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

            res = search_book_fromdb(fname, douban_books)
            if res != None:
                print(f + '  ===>  ' + res['title'])
                file_match = file_match + 1
                continue

            print(os.path.join(root, f))
            file_nomatch = file_nomatch + 1

        for d in dirs:
            if len(d) < 4 or d[-4] != '-':
                continue
            dname = d[:-4]
            res = search_book_fromdb(dname, douban_books)
            if res != None:
                print(d + '  ===>  ' + res['title'])
                file_match = file_match + 1
                continue

            print(os.path.join(root, d))
            file_nomatch = file_nomatch + 1
    return (file_match, file_nomatch)
