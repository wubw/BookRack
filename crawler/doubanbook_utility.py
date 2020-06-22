import urllib.request
from bs4 import BeautifulSoup


def getsoup(url):
    print(url)
    hdr = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Language': 'en-sg',
           'Cache-Control': 'max-age=0',
           'Cookie': 'push_doumail_num=0; push_noty_num=0; __utma=81379588.856791827.1592028653.1592646472.1592740591.18; __utmb=81379588.3.10.1592740591; __utmc=81379588; __utmz=81379588.1592122669.4.3.utmcsr=movie.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/mine; __utma=30149280.993107657.1592028653.1592646472.1592740591.24; __utmb=30149280.3.10.1592740591; __utmc=30149280; __utmv=30149280.221; __utmz=30149280.1592122669.5.2.utmcsr=movie.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/mine; _vwo_uuid_v2=D0ED8DCAD07DA13A5021BDDFF7B8727D2|d048c79dfdceb39f68ff8c26a904b67c; gr_cs1_5cca986b-f6ec-4852-a005-51a8630b1a7a=user_id%3A1; gr_user_id=1170c572-82fd-4f07-ba30-d60c7e862672; _pk_id.100001.3ac3=94348fa5e51d8645.1592028653.18.1592740602.1592647777.; _pk_ses.100001.3ac3=*; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03=5cca986b-f6ec-4852-a005-51a8630b1a7a; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03_5cca986b-f6ec-4852-a005-51a8630b1a7a=true; ap_v=0,6.0; _pk_ref.100001.3ac3=%5B%22%22%2C%22%22%2C1592740594%2C%22https%3A%2F%2Fmovie.douban.com%2Fmine%22%5D; __utmt=1; __utmt_douban=1; __gads=ID=a8457cedc56765a2-2258623c28c20067:T=1592582617:RT=1592582617:S=ALNI_MYQhZJiRZeJtub2Vtng9d_XKJiClQ; ct=y; ck=NC1x; dbcl2="2215801:q7l0wvh7FAk"; ll="108231"; bid=6oZiJHXrnh0',
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


def getbookcontent(book_url, reading_status):
    soup = getsoup(book_url)
    if soup is None:
        print('cannot get soup object')
        return None

    h1_obj = soup.find('h1')
    if h1_obj is None:
        print('cannot get book title')
        return None

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

    book_content['douban_url'] = book_url
    return book_content


def getimgdata(img_url):
    hdr = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Language': 'en-sg',
           'Accept-Encoding': 'gzip, deflate, br',
           'Connection': 'keep-alive',
           'Host': 'img9.doubanio.com'}

    try:
        with urllib.request.urlopen(img_url) as _url:
            img_data = _url.read()
        return img_data
    except Exception as ex:
        print("Exception:", ex)
    return None
