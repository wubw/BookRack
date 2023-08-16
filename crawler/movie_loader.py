from bs4 import BeautifulSoup
import os
import pandas as pd

def getsoup(path):
    f = open(path, "r", encoding='utf-8')
    soup = BeautifulSoup(f.read(), 'html.parser')
    return soup

def getmoviecontent(soup, status, movie_url):
    h1_obj = soup.find('h1')
    if h1_obj is None:
        print('cannot get movie title')
        return None

    movie_content = {}
    movie_content["title"] = h1_obj.text.strip()
    divinfo = soup.find('div', class_='subject clearfix')
    parseinfo(movie_content, divinfo.text)

    movie_content["img"] = soup.find('a', class_='nbgnbg').find('img').get('src')
    rating_strong = soup.find('strong', class_='ll rating_num')
    if rating_strong is not None:
        movie_content["rating"] = rating_strong.text.strip()
    rating_people_a = soup.find('a', class_='rating_people')
    if rating_people_a is not None:
        movie_content["ratingpeople"] = rating_people_a.find('span').text
    movie_content["watching_status"] = status
    n_rating_input = soup.find("input", {"id": "n_rating"})
    if n_rating_input is not None:
        movie_content["my_rating"] = n_rating_input.get('value')
    interest_sect_level = soup.find('div', {"id": "interest_sect_level"})
    if interest_sect_level is not None:
        interest_sect_level_find_all = interest_sect_level.find_all(
            "span", class_="color_gray")
        for elem in interest_sect_level_find_all:
            text = elem.text.strip()
            if not text:
                continue
            if text.startswith('标签'):
                movie_content["tags"] = text
            else:
                movie_content["timestamp"] = text
        my_comment_elem = interest_sect_level.find_all('span', attrs={'class': None})
        for elem in my_comment_elem:
            t = elem.text.strip()
            if len(t) == 0:
                continue
            movie_content['my_comment'] = elem.text.strip()
            break

    movie_content['douban_url'] = movie_url
    print(movie_content)
    return movie_content

def parseinfo(book_content, infotext):
    print(infotext)
    keywords_map = {
        "导演:": "director",
        "编剧:": "scriptwriter",
        "主演:": "starring",
        "类型:": "category",
        "官方网站:": "web-site",
        "制片国家/地区:": "country",
        "语言:": "language",
        "上映日期:": "date",
        "片长:": "length",
        "又名:": "othername",
        "IMDb:": "imdb",
        "首播:": "date",
        "集数:": "countinseries"
    }
    for line in infotext.splitlines():
        l = line.strip()
        if len(l) == 0:
            continue
        
        found_key = None
        for k in keywords_map.keys():
            if k in l:
                found_key = k
                break
        if found_key is None:
            continue
        v = line[len(found_key):].strip()
        book_content[keywords_map[found_key]] = v

    #book_content["info"] = infotext

def getmovie(filename, status):
    path = '../data/' + status + '/' + filename
    print(path)
    soup = getsoup(path)
    book_url = 'https://movie.douban.com/subject/' + filename[:len(filename)-len('.html')]
    #print(book_url)
    return getmoviecontent(soup, status, book_url)

#print(getmovie('1291544.html', 'will_watch'))
#print(getmovie('26761416.html', 'have_watched'))

def get_movies_from_folder(status):
    folder =  '../data/' + status
    df = None
    for f in os.listdir(folder):
        book = getmovie(f, status)
        #print(book)
        if df is None:
            df = pd.DataFrame(book, index=[0])
            continue
        df = df.append(book, ignore_index=True)

    df.to_csv('../data/' + status + '.csv', encoding='utf_8_sig')
    print(df)

#get_movies_from_folder('will_watch')
#get_movies_from_folder('watching')
get_movies_from_folder('have_watched')