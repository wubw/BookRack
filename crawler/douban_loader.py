from bs4 import BeautifulSoup
import os
import pandas as pd

def getsoup(path):
    f = open(path, "r", encoding='utf-8')
    soup = BeautifulSoup(f.read(), 'html.parser')
    return soup

def getbookcontent(soup, reading_status, book_url):
    h1_obj = soup.find('h1')
    if h1_obj is None:
        print('cannot get book title')
        return None

    book_content = {}
    book_content["title"] = h1_obj.text.strip()
    divinfo = soup.find('div', class_='subject clearfix')
    parseinfo(book_content, divinfo.text)

    book_content["img"] = soup.find('a', class_='nbg').find('img').get('src')
    rating_strong = soup.find('strong', class_='ll rating_num')
    if rating_strong is not None:
        book_content["rating"] = rating_strong.text.strip()
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
        my_comment_elem = interest_sect_level.find_all('span', attrs={'class': None})
        for elem in my_comment_elem:
            book_content['my_comment'] = elem.text.strip()
            break

    book_content['douban_url'] = book_url
    return book_content

def parseinfo(book_content, infotext):
    print(infotext)
    arr = []
    keywords_map = {
        "作者:": "author",
        "出版社:": "publisher",
        "副标题:": "sub-title",
        "出版年:": "publish-year",
        "页数:": "page-cnt",
        "丛书:": "series",
        "ISBN:": "ISBN"
    }
    keyword_identified = None
    for line in infotext.splitlines():
        l = line.strip()
        if len(l) == 0:
            continue
        
        found_key = None
        for k in keywords_map.keys():
            if k in l:
                found_key = k
                break

        if found_key is None and ":" in l:
            continue

        if keyword_identified is None and found_key is None:
            continue

        if keyword_identified is not None and found_key is None:
            keyword_identified = keyword_identified + l
            continue

        if keyword_identified is None and found_key is not None:
            keyword_identified = found_key
            continue

        if keyword_identified is not None and found_key is not None:
            arr.append(keyword_identified)
            keyword_identified = l
            continue

    if keyword_identified is not None:
        arr.append(keyword_identified)
    print(arr)

    for elem in arr:
        for k in keywords_map.keys():
            if elem.startswith(k):
                v = elem[len(k):].strip()
                book_content[keywords_map[k]] = v

    #book_content["info"] = infotext

def getbook(filename, reading_status):
    path = '../data/' + reading_status + '/' + filename
    print(path)
    soup = getsoup(path)
    book_url = 'https://book.douban.com/subject/' + filename[:len(filename)-len('.html')]
    #print(book_url)
    return getbookcontent(soup, 'have_read', book_url)

#print(getbook('25857796.html', 'will_read'))

def get_books_from_folder(reading_status):
    folder =  '../data/' + reading_status
    df = None
    for f in os.listdir(folder):
        book = getbook(f, reading_status)
        #print(book)
        if df is None:
            df = pd.DataFrame(book, index=[0])
            continue
        df = df.append(book, ignore_index=True)

    df.to_csv('../data/' + reading_status + '.csv', encoding='utf_8_sig')
    print(df)

get_books_from_folder('will_read')
#get_books_from_folder('reading')
get_books_from_folder('have_read')