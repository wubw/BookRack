import urllib
import urllib.request
import os
from bs4 import BeautifulSoup
import sys

print(sys.version)

downloaded_books = []
downloaded_filename = '../data/downloaded.txt'
if os.path.isfile(downloaded_filename):
    downloaded_file = open(downloaded_filename, 'r')
    downloaded_books = downloaded_file.read().splitlines()
    downloaded_file.close()

def handlebookspage(booklist_url, start, tag):
    url_postfix = '&sort=time&rating=all&filter=all&mode=grid'
    url = booklist_url + str(start) + url_postfix
    page_count = 15
    print(url)
#    with urllib.request.urlopen(url) as url_reader:
#        s = url_reader.read()
    hdr = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.8,no;q=0.6,nb;q=0.4,nn;q=0.2,en-GB;q=0.2,zh-CN;q=0.2,zh;q=0.2,zh-TW;q=0.2,ja;q=0.2,en-AU;q=0.2,en-CA;q=0.2',
        'Cache-Control': 'max-age=0',
        'Cookie': 'll="128467"; bid=fpLY7QWblWQ; gr_user_id=4f09d8f1-9c09-4b8c-a52e-2becf082bd04; ue="summersnowe@gmail.com"; viewed="6850304_1979199_26759508"; _ga=GA1.2.667707122.1469459924; dbcl2="2215801:VtSDS+esh4g"; ck=ltpE; _vwo_uuid_v2=4EA37F5A34C953286AEEC1D971D5DCEC|efafbe71eb587cec38b4b8dadca81511; _pk_ref.100001.3ac3=%5B%22%22%2C%22%22%2C1480865161%2C%22https%3A%2F%2Fmovie.douban.com%2F%22%5D; push_noty_num=0; push_doumail_num=0; _pk_id.100001.3ac3=c2dd158ed28051a5.1469460792.28.1480865315.1480845651.; __utma=30149280.667707122.1469459924.1480844586.1480865161.41; __utmc=30149280; __utmz=30149280.1475409046.30.5.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmv=30149280.221; __utma=81379588.1703314858.1469460791.1480844605.1480865161.28; __utmc=81379588; __utmz=81379588.1480844605.27.22.utmcsr=movie.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/',
        'Upgrade-Insecure-Requests': '1',
        'Connection': 'keep-alive'}
    req = urllib.request.Request(url, headers=hdr)
    s = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(s, 'lxml')
    findings = soup.find_all('a', class_='nbg')
    finding_count = 0
    for f in findings:
        getbookitem(f.get('href'), tag)
        finding_count = finding_count + 1
    if finding_count == page_count:
        handlebookspage(booklist_url, start + page_count, tag)

def getbookitem(book_url, tag):
    if book_url in downloaded_books:
        return
    try:
        soup = getsoup(book_url)
    except:
        print("Http error")
        return
    h1_obj = soup.find('h1')
    if h1_obj is None:
        print('cannot get book title')
        return
    book_title = h1_obj.text.strip()
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
    downloaded_file = open(downloaded_filename, 'a')
    downloaded_file.write(book_url + '\n')
    downloaded_file.close()

def getsoup(book_url):
    print(book_url)
    with urllib.request.urlopen(book_url) as url:
        s = url.read()
    soup = BeautifulSoup(s, 'lxml')
    return soup

handlebookspage("https://book.douban.com/people/wubinwei/collect?start=", 0, 'have_read')
handlebookspage("https://book.douban.com/people/wubinwei/do?start=", 0, 'reading')
handlebookspage("https://book.douban.com/people/wubinwei/wish?start=", 0, 'will_read')

