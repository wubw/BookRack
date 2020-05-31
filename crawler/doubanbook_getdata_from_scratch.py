import urllib.request
import os
import doubanbook_utility
from bs4 import BeautifulSoup
import time


def handlebookspage(booklist_url, start, reading_status):
    url_postfix = '&sort=time&rating=all&filter=all&mode=grid'
    url = booklist_url + str(start) + url_postfix
    soup = doubanbook_utility.getsoup(url)
    if soup is None:
        print('cannot get soup object')
        return

    time.sleep(5)
    subject_item_list = soup.find_all('a', class_='nbg')
    finding_count = 0
    for f in subject_item_list:
        getbookitem(f.get('href'), reading_status)
        finding_count = finding_count + 1

    if finding_count > 0:
        handlebookspage(booklist_url, start + finding_count, reading_status)


def getbookitem(book_url, reading_status):
    if book_url in downloaded_books:
        return

    book_content = doubanbook_utility.getbookcontent(book_url, reading_status)
    if book_content != None:
        serializebookitem(book_url, book_content)


def serializebookitem(book_url, book_content):
    print(book_content)
    data_dir = '../data'
    book_dir = os.path.join(data_dir, book_content["title"])
    if not os.path.exists(book_dir):
        os.makedirs(book_dir)
    file_path = os.path.join(book_dir, 'book')
    f = open(file_path, 'wb+')
    f.write((str(book_content).encode('utf-8')))
    f.close()
    cover_path = os.path.join(book_dir, 'cover.jpg')
    try:
        urllib.request.urlretrieve(book_content["img"], cover_path)
    except Exception as ex:
        print("Exception:", ex)

    downloaded_file = open(downloaded_filename, 'a')
    downloaded_file.write(book_url + '\n')
    downloaded_file.close()


downloaded_books = []
downloaded_filename = '../data/downloaded.txt'
if os.path.isfile(downloaded_filename):
    downloaded_file = open(downloaded_filename, 'r')
    downloaded_books = downloaded_file.read().splitlines()
    downloaded_file.close()

# handlebookspage(
#     "https://book.douban.com/people/wubinwei/collect?start=", 0, 'have_read')
# handlebookspage(
#     "https://book.douban.com/people/wubinwei/do?start=", 0, 'reading')
# handlebookspage(
#     "https://book.douban.com/people/wubinwei/wish?start=", 0, 'will_read')

getbookitem('https://book.douban.com/subject/1025643/', 'have_read')
getbookitem('https://book.douban.com/subject/1674929/', 'have_read')
