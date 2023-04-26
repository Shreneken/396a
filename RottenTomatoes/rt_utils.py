from bs4 import BeautifulSoup
from requests import get
from datetime import datetime
import json
import time
import os

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}

def change_title_if_required(title):
    if ':' in title:
        title = "--".join(title.split(':'))
    if '?' in title:
        title = "(question_mark)".join(title.split('?'))
    if '/' in title:
        title = "(slash)".join(title.split('/'))
    if ',' in title:
        title = "(comma)".join(title.split('comma'))
    return title

def check_file_existence(file_name):
    already_exists = False
    file_name = change_title_if_required(file_name)
    if "rt_movie_jsons" in os.listdir("./RottenTomatoes"):
        for json_name in os.listdir("./RottenTomatoes/rt_movie_jsons"):
            if file_name in json_name:
                already_exists = True
                break
        return already_exists


def get_movie_url(title):
    search_url = "https://www.rottentomatoes.com/search?search=" + title.lower().replace(' ', '-')
    while True:
        try:
            search_results = get(search_url, headers=HEADERS)
            break
        except Exception:
            print("Connection failed.. Retrying")
            time.sleep(0.1)
    chicken = BeautifulSoup(search_results.content, "html.parser")
    movie_url = chicken.find_all('search-page-media-row')
    if movie_url is None:
        return "Movie not found"
    else:
        for movie in movie_url:
            movie_name = movie.find('a', attrs ={'data-qa': 'info-name'}).string.strip()
            score = movie['tomatometerscore']
            if score != 'null' and score != '':
                print(movie_name)
                print(score)
                return movie.find('a')['href']
        return movie_url[0]

def find_movie_id(soup):
    try:
        id = soup.find('critic-add-article')['emsid']
        return id
    except Exception:
        return ''

def find_rating(soup):
    try:
        rt_str = soup.find('score-board')['audiencescore']
        rating = float(rt_str) / 10
        return rating
    except Exception:
        return 0.0

def find_release_date(soup):
    try:
        rd_str = soup.find('time').string
        dt = datetime.strptime(rd_str,"%b %d, %Y")
        rd = str(dt.date())
        return rd
    except Exception:
        return 'Invalid'

def find_genres(soup):
    try:
        genre_containers = soup.find_all('li', attrs={'class': 'info-item'})
        genre_container = genre_containers[1]
        genres_str = genre_container.find('p').find('span').string.strip().replace(" ", "").replace("\n", "")
        if ',' in genres_str:
            genres = genres_str.split(',')
        else:
            genres = [genres_str]
        return genres
    except Exception:
        return []

def find_summary(soup):
    try:
        summary = soup.find('p', attrs={'data-qa': 'movie-info-synopsis'}).string.strip()
        return summary
    except Exception:
        return 'N/A'

def find_director(soup):
    try:
        director = soup.find('a', attrs={'data-qa': 'movie-info-director'}).string
        return director
    except Exception:
        return 'unknown'

def movie_into_json(content, movie_title, release_date, director):
    try:
        with open(
            f"./RottenTomatoes/rt_movie_jsons/{movie_title}-{release_date}-{director}.json", "w"
        ) as eachMovie:
            json.dump(content, eachMovie, indent=4)
    except:
        print(f"./RottenTomatoes/rt_movie_jsons/{movie_title}-{release_date}-{director}.json")
        with open(
            f"./RottenTomatoes/rt_movie_jsons/{movie_title}-{release_date}-{director}.json", "w"
        ) as eachMovie:
            json.dump(content, eachMovie, index=4)