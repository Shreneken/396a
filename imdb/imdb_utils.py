import json
from bs4 import BeautifulSoup
from requests import get
import os 

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
    "Accept-Encoding": "gzip, deflate",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "DNT": "1",
    "Connection": "close",
    "Upgrade-Insecure-Requests": "1",
}

def writeMovieIntoJsonFile(content, movie_title, release_date, director):
    try:
        with open(f"./imdb_movie_jsons/{movie_title}-{release_date}-{director}.json","w") as eachMovie:
            json.dump(content,eachMovie)
    except:
        os.mkdir("./imdb_movie_jsons")
        with open(f"./imdb_movie_jsons/{movie_title}-{release_date}-{director}.json","w") as eachMovie:
            json.dump(content,eachMovie)
def check_status_code(sc1,sc2):
    return all([check(sc1),check(sc2)])

def check(sc1):
    return sc1 == 200

def loadJSONintoDict(JSONname):
    with open(JSONname,"r") as dbData:
        data = json.load(dbData)
    return data

def getData():
    data = {}
    # Request top 250 movies page from imdB
    top_250_movies = get(
        "https://www.imdb.com/chart/top/?ref_=nv_mp_mv250", headers=HEADERS
    )
    # Using HTML parser from BeautifulSoup on our request
    checkBs = BeautifulSoup(top_250_movies.content, "html.parser")

    # Get all <td class= titleColumn> elements in a list
    titles = checkBs.find_all("td", class_="titleColumn")

    # Initiate data[movie_name] = [] to all movies in the list
    for t in titles:
        data[t.select("a")[0].text] = []

    # Get watchlistColumn for title id and ratingColumn for ratings
    watchlistColumn = checkBs.find_all("td", class_="watchlistColumn")
    ratings = checkBs.find_all("td", class_="ratingColumn imdbRating")

    # Add titleid and rating to each corresponding movie
    for t, id, r in zip(data, watchlistColumn, ratings):
        data[t].append({"id": id.div["data-tconst"]})
        data[t].append({"rating": r.select("strong")[0].text})
    
    return data