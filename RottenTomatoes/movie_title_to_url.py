from requests import get
import json
from bs4 import BeautifulSoup

with open("./movie_urls.json", "r") as urls:
    url = json.load(urls)

with open("../movie_titles_list.json", "r") as mlist:
    movies = json.load(mlist)

for i in range(0, len(movies)):
    # movie name
    name = movies[i]
    # search parameter
    search_url = "https://www.rottentomatoes.com/search?search=" + name.lower().replace(' ', '-')
    # the movie url
    try:
        search_results = get(search_url)
        soup = BeautifulSoup(search_results.content, "html.parser")
        movie_url = soup.find('search-page-media-row').find('a').attrs[0]
        url[name] = movie_url
    except Exception:
        continue

with open("./RottenTomatoes/movie_urls.json", "w") as urls_list:
    json.dump(url, urls_list)