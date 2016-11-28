import urllib
import urllib.request
import os
from bs4 import BeautifulSoup

def handlebookspage(booklist_url, tag):
    print(booklist_url)
    with urllib.request.urlopen(booklist_url) as url:
        s = url.read()
    soup = BeautifulSoup(s, 'lxml')
    findings = soup.find_all('a', class_='nbg')
    for f in findings:
        getbookitem(f.get('href'), tag)

def getbookitem(book_url, tag):
    print(book_url)
    with urllib.request.urlopen(book_url) as url:
        s = url.read()
    soup = BeautifulSoup(s, 'lxml')
    book_title = soup.find('h1').text.strip()
    divinfo = soup.find('div', class_='subject clearfix')
    book_info = ' '.join(divinfo.text.split())
    book_img = soup.find('a', class_='nbg').find('img').get('src')
    book_rating = soup.find('strong', class_='ll rating_num')
    ratingpeople = soup.find('a', class_='rating_people')

    data_dir = '../data'
    book_dir = os.path.join(data_dir, book_title)
    if not os.path.exists(book_dir):
        os.makedirs(book_dir)
    file_path = os.path.join(book_dir, 'book')
    f = open(file_path, 'wb+')
    f.write((book_info+'\n').encode('utf-8'))
    if book_rating:
        f.write((book_rating+'\n').encode('utf-8'))
    if ratingpeople:
        f.write((ratingpeople.text+'\n').encode('utf-8'))
    f.write(tag.encode('utf-8'))
    f.close()
    cover_path = os.path.join(book_dir, 'cover.jpg')
    urllib.request.urlretrieve(book_img, cover_path)

    print(book_title)

handlebookspage("https://book.douban.com/people/wubinwei/do", 'reading')
handlebookspage("https://book.douban.com/people/wubinwei/wish", 'will_read')
