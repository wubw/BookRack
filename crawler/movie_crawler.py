import urllib.request
from bs4 import BeautifulSoup
import time
import random
import os.path
import logging

logging.basicConfig(filename='crawler.log', encoding='utf-8', level=logging.DEBUG)
process_moviepages_file = open("processed_moviepages.txt", "a")  # append mode


def getsoup(url):
    print(url)
    hdr = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Language': 'en-sg',
           'Cache-Control': 'max-age=0',
           #'Cookie': 'push_doumail_num=0; push_noty_num=0; __utma=81379588.856791827.1592028653.1592646472.1592740591.18; __utmb=81379588.3.10.1592740591; __utmc=81379588; __utmz=81379588.1592122669.4.3.utmcsr=movie.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/mine; __utma=30149280.993107657.1592028653.1592646472.1592740591.24; __utmb=30149280.3.10.1592740591; __utmc=30149280; __utmv=30149280.221; __utmz=30149280.1592122669.5.2.utmcsr=movie.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/mine; _vwo_uuid_v2=D0ED8DCAD07DA13A5021BDDFF7B8727D2|d048c79dfdceb39f68ff8c26a904b67c; gr_cs1_5cca986b-f6ec-4852-a005-51a8630b1a7a=user_id%3A1; gr_user_id=1170c572-82fd-4f07-ba30-d60c7e862672; _pk_id.100001.3ac3=94348fa5e51d8645.1592028653.18.1592740602.1592647777.; _pk_ses.100001.3ac3=*; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03=5cca986b-f6ec-4852-a005-51a8630b1a7a; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03_5cca986b-f6ec-4852-a005-51a8630b1a7a=true; ap_v=0,6.0; _pk_ref.100001.3ac3=%5B%22%22%2C%22%22%2C1592740594%2C%22https%3A%2F%2Fmovie.douban.com%2Fmine%22%5D; __utmt=1; __utmt_douban=1; __gads=ID=a8457cedc56765a2-2258623c28c20067:T=1592582617:RT=1592582617:S=ALNI_MYQhZJiRZeJtub2Vtng9d_XKJiClQ; ct=y; ck=NC1x; dbcl2="2215801:q7l0wvh7FAk"; ll="108231"; bid=6oZiJHXrnh0',
           'Cookie': 'gr_user_id=4a739ff1-06de-4e62-b50f-d0794972093e; __utmv=30149280.221; _vwo_uuid_v2=DE7A37547519A30210535E06D5352A0C1|43c5797bed9542ac6533ccfd90bdf4e6; _ga=GA1.1.668565849.1668421646; push_noty_num=0; push_doumail_num=0; bid=oNuG3PutWeU; _pk_id.100001.4cf6=38c4de9613e90479.1667364821.; __utmz=30149280.1684242040.121.9.utmcsr=book.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmz=223695111.1684242040.3.1.utmcsr=book.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; _ga_RXNMP372GL=GS1.1.1687328706.3.0.1687328714.52.0.0; dbcl2="2215801:vVwX5sKXuuE"; ck=NVW9; __utmc=30149280; frodotk_db="c7fcb0fb3b81d2db57f612f1b2857891"; __utmc=223695111; ap_v=0,6.0; __utma=30149280.297989026.1647833514.1692005234.1692007196.149; __utma=223695111.1874489744.1667364821.1692005234.1692007196.5; __utmb=223695111.0.10.1692007196; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1692007196%2C%22https%3A%2F%2Fbook.douban.com%2F%22%5D; _pk_ses.100001.4cf6=1; __gads=ID=f09b5f7efb892976-22b0e5d12cdf00b0:T=1681701965:RT=1692007233:S=ALNI_MZcsn4ypOOF4oTxoXqOY6rGUdFDfw; __gpi=UID=00000c21686a8f98:T=1689567521:RT=1692007233:S=ALNI_MZi2639QzcgGjCy9IO52YmriFbtRA; __utmt=1; __utmb=30149280.6.10.1692007196',
           'Upgrade-Insecure-Requests': '1',
           'Connection': 'keep-alive'}
    req = urllib.request.Request(url, headers=hdr)

    try:
        with urllib.request.urlopen(req) as _url:
            s = _url.read()
        return BeautifulSoup(s, 'lxml')
    except Exception as ex:
        logging.warning("Exception: " + str(ex) + ', ' + url)

    return None

def crawl_moviepage(url, status):
    process_moviepages_file.write(url + "\n")

    prefix = 'https://movie.douban.com/subject/'
    id = None
    if url.startswith(prefix):
        id = url[len(prefix):-1]
    if id is None:
        logging.warning('cannot get id from url: ' + url) 
        return
    
    soup = getsoup(url)

    path = '../data/' + status + '/' + id + '.html'
    if os.path.exists(path):
        print('file exists: ' + path)
        return
    
    with open(path, "w", encoding='utf-8') as file:
        file.write(str(soup))

#crawl_moviepage('https://movie.douban.com/subject/26268602/', 'watching')

def handlemoviespage(movielist_url, start, status):
    url_postfix = '&sort=time&filter=all&mode=list&tags_sort=count'
    url = movielist_url + str(start) + url_postfix
    soup = getsoup(url)
    if soup is None:
        logging.warning('cannot get soup object: ' + url) 
        return

    time.sleep(random.randint(0, 9))

    subject_item_list = soup.find_all('div', class_='title')
    finding_count = 0
    for f in subject_item_list:
        a = f.find('a')
        url = a.get('href')
        time.sleep(0.1*random.randint(0, 9))
        print(a.text.strip())
        crawl_moviepage(url, status)

        finding_count = finding_count + 1

    if finding_count > 0:
        handlemoviespage(movielist_url, start + finding_count, status)

#handlemoviespage("https://movie.douban.com/people/wubinwei/collect?start=", 0, 'have_watched')
#handlemoviespage("https://movie.douban.com/people/wubinwei/do?start=", 0, 'watching')
handlemoviespage("https://movie.douban.com/people/wubinwei/wish?start=", 0, 'will_watch')

process_moviepages_file.close()

def found_deleted_movies(booklist_url, start, reading_status):
    deleted_files = [
        "https://movie.douban.com/subject/1424420/",
        "https://movie.douban.com/subject/1456692/",
        "https://movie.douban.com/subject/35796153/"
    ]
    url_postfix = '&sort=time&filter=all&mode=list&tags_sort=count'
    url = booklist_url + str(start) + url_postfix
    soup = getsoup(url)
    if soup is None:
        logging.warning('cannot get soup object: ' + url) 
        return

    time.sleep(random.randint(0, 9))

    subject_item_list = soup.find_all('div', class_='title')
    finding_count = 0
    for f in subject_item_list:
        a = f.find('a')
        url = a.get('href')
        time.sleep(0.1*random.randint(0, 9))

        if url in deleted_files:
            logging.warning(a.text.strip() + '-> ' +  url) 
            print(a.text.strip())
            print(url)

        finding_count = finding_count + 1

    if finding_count > 0:
        found_deleted_movies(booklist_url, start + finding_count, reading_status)

#found_deleted_movies("https://book.douban.com/people/wubinwei/collect?start=", 0, 'have_read')
#found_deleted_book("https://book.douban.com/people/wubinwei/do?start=", 0, 'reading')
#found_deleted_movies("https://book.douban.com/people/wubinwei/wish?start=", 930, 'will_read')