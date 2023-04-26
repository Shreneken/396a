from bs4 import BeautifulSoup
import requests
import rt_utils as rt
from datetime import datetime
import json
import time
from tqdm import tqdm
import re

HEADERS = rt.HEADERS

with open("./movie_titles_list.json", "r") as mlist:
    movies = json.load(mlist)

for title in tqdm(movies):

    #check if file already exists
    already_exists = rt.check_file_existence(title)
    if already_exists:
        continue
    
    #movie and review pages' urls
    movie_url = rt.get_movie_url(title)

    if movie_url == "Movie not found":
        continue

    while True:
        try:
            movie = requests.get(movie_url, headers=HEADERS)
            break
        except Exception:
            print("Connection failed.. Retrying")
            time.sleep(0.1)

    #parsing trees for all pages
    soup = BeautifulSoup(movie.content, "lxml")

    #movie details
    rating = rt.find_rating(soup)
    release_date = rt.find_release_date(soup)
    genres = rt.find_genres(soup)
    summary = rt.find_summary(soup)
    movie_id = rt.find_movie_id(soup)
    director = rt.find_director(soup)

    #initialize to empty list
    reviews = []

    api_url = "https://www.rottentomatoes.com/napi/movie/" + movie_id + "/reviews/user"

    while True:
        try:
            api = requests.get(api_url, headers=HEADERS)
            break
        except Exception:
            print("Connection failed.. Retrying")
            time.sleep(0.1)

    wonton = BeautifulSoup(api.content, "lxml")

    #first page
    content_string = wonton.find('body').contents[0].string
    content_obj = json.loads(content_string)

    if len(content_obj) != 0:
        for review in content_obj["reviews"]:
            rev = {}
            rev["content"] = review["quote"]
            rev["review_date"] =  str(datetime.strptime(review["creationDate"],"%b %d, %Y").date())
            rev["source"] = "rt"
            reviews.append(rev)

    #the rest of the pages
    hasNextPage = content_obj["pageInfo"]["hasNextPage"]

    while hasNextPage:
        endCursor = content_obj["pageInfo"]["endCursor"]
        next_url = "https://www.rottentomatoes.com/napi/movie/" + movie_id + "/reviews/user?after=" + endCursor
    
        while True:
            try:
                next = requests.get(next_url, headers=HEADERS)
                break
            except Exception:
                print("Connection failed.. Retrying")
                time.sleep(0.1)

        cheddar = BeautifulSoup(next.content, "lxml")

        try:
            content_string = cheddar.find('body').contents[0].string
            content_obj = json.loads(content_string)
        except Exception:
            print(next_url)
            break


        if len(content_obj) != 0:
            for review in content_obj["reviews"]:
                rev = {}
                rev["content"] = review["quote"]
                rev["review_date"] =  str(datetime.strptime(review["creationDate"],"%b %d, %Y").date())
                rev["source"] = "rt"
                reviews.append(rev)

        hasNextPage = content_obj["pageInfo"]["hasNextPage"]

    num_reviews = len(reviews)

    content = {"rating" : rating,
               "release_date" : release_date,
               "num_reviews" : num_reviews,
               "genres" : genres,
               "summary" : summary,
               "reviews" : reviews}

    title = rt.change_title_if_required(title)
    rt.movie_into_json(content, title, release_date, director)