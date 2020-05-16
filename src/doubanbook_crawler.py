import urllib.request
import os
from bs4 import BeautifulSoup
import time


def getsoup(url):
    print(url)
    hdr = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Language': 'en-sg',
           'Cache-Control': 'max-age=0',
           'Cookie': '__utma=81379588.1243558140.1585669813.1589622269.1589627340.98; __utmb=81379588.202.10.1589627340; __utmc=81379588; __utmz=81379588.1589597487.96.14.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utma=30149280.1930022656.1585669813.1589622269.1589627340.107; __utmb=30149280.202.10.1589627340; __utmc=30149280; __utmv=30149280.221; __utmz=30149280.1589597484.105.11.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/passport/login; push_doumail_num=0; push_noty_num=0; _pk_id.100001.3ac3=b8c3de2bd3e29135.1585669813.100.1589634346.1589623401.; _pk_ses.100001.3ac3=*; __utmt=1; __utmt_douban=1; _vwo_uuid_v2=D0ED8DCAD07DA13A5021BDDFF7B8727D2|d048c79dfdceb39f68ff8c26a904b67c; gr_cs1_f86ad958-b02e-4f21-9546-4b6dc4a33824=user_id%3A1; gr_user_id=1170c572-82fd-4f07-ba30-d60c7e862672; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03=f86ad958-b02e-4f21-9546-4b6dc4a33824; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03_f86ad958-b02e-4f21-9546-4b6dc4a33824=true; ap_v=0,6.0; ct=y; _pk_ref.100001.3ac3=%5B%22%22%2C%22%22%2C1589627340%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; __gads=ID=3c8133b4397007b6:T=1589623256:S=ALNI_MbA1g4saW_RXpFr2XteqskxsJz3Rw; dbcl2="2215801:1IapRb8S1vk"; ck=rN1_; douban-profile-remind=1; Hm_lvt_cfafef0aa0076ffb1a7838fd772f844d=1586671023,1586671369,1589078698; ll="108231"; bid=6oZiJHXrnh0',
           'Upgrade-Insecure-Requests': '1',
           'Connection': 'keep-alive'}
    req = urllib.request.Request(url, headers=hdr)

    try:
        with urllib.request.urlopen(req) as _url:
            s = _url.read()
        return BeautifulSoup(s, 'lxml')
    except Exception as ex:
        print("Exception:", ex)

    return None


def handlebookspage(booklist_url, start, reading_status):
    url_postfix = '&sort=time&rating=all&filter=all&mode=grid'
    url = booklist_url + str(start) + url_postfix
    soup = getsoup(url)
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

    soup = getsoup(book_url)
    if soup is None:
        print('cannot get soup object')
        return

    time.sleep(5)
    h1_obj = soup.find('h1')
    if h1_obj is None:
        print('cannot get book title')
        return

    book_content = {}
    book_content["title"] = h1_obj.text.strip()
    divinfo = soup.find('div', class_='subject clearfix')
    book_content["info"] = '||'.join(divinfo.text.split())
    book_content["img"] = soup.find('a', class_='nbg').find('img').get('src')
    book_content["rating"] = soup.find(
        'strong', class_='ll rating_num').text.strip()
    rating_people_a = soup.find('a', class_='rating_people')
    if rating_people_a is not None:
        book_content["ratingpeople"] = rating_people_a.find('span').text
    book_content["reading_status"] = reading_status
    n_rating_input = soup.find("input", {"id": "n_rating"})
    if n_rating_input is not None:
        book_content["my_rating"] = n_rating_input.get('value')
    interest_sect_level = soup.find('div', {"id": "interest_sect_level"})
    if interest_sect_level is not None:
        interest_sect_level_find_all = interest_sect_level.find_all(
            "span", class_="color_gray")
        for elem in interest_sect_level_find_all:
            text = elem.text.strip()
            if not text:
                continue
            if text.startswith('标签'):
                book_content["tags"] = text
            else:
                book_content["timestamp"] = text

    serializebookitem(book_url, book_content)
    # wait for a while


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

handlebookspage(
    "https://book.douban.com/people/wubinwei/collect?start=", 0, 'have_read')
handlebookspage(
    "https://book.douban.com/people/wubinwei/do?start=", 0, 'reading')
handlebookspage(
    "https://book.douban.com/people/wubinwei/wish?start=", 0, 'will_read')
