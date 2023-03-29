from requests import get
import json
from bs4 import BeautifulSoup
import os

data = {}

with open("./movie_titles_list.json", "r") as mlist:
    movies = json.load(mlist)

for i in range(0, len(movies)):
    # movie name
    name = movies[i]
    # search parameter
    search_url = "https://www.rottentomatoes.com/search?search=" + name.lower().replace(' ', '-')
    # the movie url
    search_results = get(search_url, headers=headers)
    soup = BeautifulSoup(search_results.content, "html.parser")
    movie_url = soup.find('search-page-media-row')
    if movie_url != "None":
        movie_url = movie_url.find('a').attrs['href']
        data[name] = movie_url
    else:
        data[name] = ""

with open("./RottenTomatoes/movie_urls.json", "w") as urls_list:
    json.dump(data, urls_list)