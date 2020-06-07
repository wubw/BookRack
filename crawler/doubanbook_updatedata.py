import doubanbook_utility
import random
import time
import pymongo
import urllib.request
import base64

mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["books"]
mongo_col = mongo_db["douban"]

doubanbooks = []


def handlebookspage(booklist_url, start, reading_status):
    url_postfix = '&sort=time&filter=all&mode=list&tags_sort=count'
    url = booklist_url + str(start) + url_postfix
    soup = doubanbook_utility.getsoup(url)
    if soup is None:
        print('cannot get soup object')
        return

    time.sleep(random.randint(0, 9))

    subject_item_list = soup.find_all('div', class_='title')
    finding_count = 0
    for f in subject_item_list:
        b = {}
        a = f.find('a')
        b['douban_url'] = a.get('href')
        b['title'] = a.text.strip()
        doubanbooks.append(b)
        find_book = mongo_col.find_one(
            {"douban_url": b['douban_url']})
        if find_book == None:
            print("insert new book into mongodb:")
            print(b)
            book_content = doubanbook_utility.getbookcontent(
                b['douban_url'], reading_status)
            img_data = urllib.request.urlopen(book_content['img']).read()
            book_content['img_data'] = base64.encodebytes(
                img_data).decode("utf-8")
            # print(book_content)
            mongo_col.insert_one(book_content)
        else:
            if find_book['reading_status'] != reading_status:
                print('update book reading status from ' + find_book['reading_status'] +
                      ' to ' + reading_status)
                print(b)
                result = mongo_col.update_one(
                    {"douban_url": b['douban_url']},
                    {"$set": {"reading_status": reading_status}},
                    upsert=True)

        finding_count = finding_count + 1

    if finding_count > 0:
        handlebookspage(booklist_url, start + finding_count, reading_status)


# handlebookspage(
#     "https://book.douban.com/people/wubinwei/collect?start=", 0, 'have_read')
# handlebookspage(
#    "https://book.douban.com/people/wubinwei/do?start=", 0, 'reading')
# handlebookspage(
#    "https://book.douban.com/people/wubinwei/wish?start=", 0, 'will_read')

# print(doubanbooks)

def process_info_property(book):
    info = book['info']
    if info == None:
        return
    if 'author' in book:
        return

    splits = info.split('||')
    searchkeywords = {
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
    }

    tempBuf = []
    searchKey = ""
    results = {}
    for elem in splits:
        if elem in searchkeywords:
            if searchKey:
                results[searchKey] = " ".join(tempBuf)
            tempBuf = []
            searchKey = searchkeywords[elem]
            continue
        if searchKey:
            tempBuf.append(elem)

    for k in results:
        mongo_col.update_one(
            {"_id": book['_id']},
            {"$set": {k: results[k]}},
            upsert=True)


for book in mongo_col.find():
    process_info_property(book)
