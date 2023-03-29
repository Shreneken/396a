from requests import get
import datetime
import json
from bs4 import BeautifulSoup
import rt_utils as rt
import time

HEADERS = rt.HEADERS

with open("./movie_titles_list.json", "r") as mlist:
    movies = json.load(mlist)
    movies = [movies[0]]

for title in movies:
    #check if file already exists
    already_exists = rt.check_file_existence(title)
    if already_exists:
        continue
    
    #movie and review pages' urls
    movie_url = rt.get_movie_url(title)
    print(movie_url)

    if movie_url == "Movie not found":
        continue

    rev_critics_url = movie_url + "/reviews"
    rev_audience_url = movie_url + "/reviews?type=user"

    while True:
        try:
            movie = get(movie_url, headers=HEADERS)
            rev_critics = get(rev_critics_url, headers=HEADERS)
            rev_audience = get(rev_audience_url, headers=HEADERS)
            break
        except Exception:
            print("Connection failed.. Retrying")
            time.sleep(0.1)

    #parsing trees for all pages
    soup = BeautifulSoup(movie.content, "html.parser")
    tomato = BeautifulSoup(rev_critics.content, "html.parser")
    wonton = BeautifulSoup(rev_audience.content, "html.parser")

    rating = rt.find_rating(soup)
    release_date = rt.find_release_date(soup)
    # genres = rt.find_genres(soup)
    summary = rt.find_summary(soup)
    num_reviews = 0


