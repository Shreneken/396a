import json
from bs4 import BeautifulSoup
from requests import get
import os
from datetime import datetime

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
    "Accept-Encoding": "gzip, deflate",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "DNT": "1",
    "Connection": "close",
    "Upgrade-Insecure-Requests": "1",
}


def movie_into_json(content, movie_title, release_date, director):
    try:
        with open(
            f"./imdb/imdb_movie_jsons/{movie_title}-{release_date}-{director}.json", "w"
        ) as eachMovie:
            json.dump(content, eachMovie, indent=4)
    except:
        print(f"./imdb/imdb_movie_jsons/{movie_title}-{release_date}-{director}.json")
        os.mkdir("./imdb/imdb_movie_jsons")
        with open(
            f"./imdb/imdb_movie_jsons/{movie_title}-{release_date}-{director}.json", "w"
        ) as eachMovie:
            json.dump(content, eachMovie, index=4)


def check_status_code(sc1, sc2):
    return all([check(sc1), check(sc2)])


def check(sc1):
    return sc1 == 200


def loadJSONintoDict(JSONname):
    with open(JSONname, "r") as dbData:
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


def find_director(congee):
    director_container = congee.find_all(
        "a",
        class_="ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link",
    )
    director_indexed = director_container[0]
    director = director_indexed.string
    return director


def find_release_date(congee):
    release_date_container = congee.find_all(
        "ul",
        class_="ipc-metadata-list ipc-metadata-list--dividers-all ipc-metadata-list--base",
    )
    if len(release_date_container) == 0: 
        release_date = "Invalid"
    else:
        try:
            release_date_indexed = release_date_container[0]
            release_date_arr = release_date_indexed.select("li div ul li a")[0].text.split(
                " "
            )[:3]
        except IndexError:
            release_date_indexed = release_date_container[1]
            release_date_arr = release_date_indexed.select("li div ul li a")[0].text.split(
                " "
            )[:3]
        try:
            release_date_str = " ".join(release_date_arr)
            datetime_object = datetime.strptime(release_date_str, "%B %d, %Y")
            release_date = str(datetime_object.date())
        except ValueError:
            release_date = " ".join(release_date_arr)
    return release_date


def find_genre(congee):
    genre_list = []
    genres = congee.select_one("div.ipc-chip-list__scroller")
    try:
        for genre in genres.contents:
            genre_list.append(genre.text)
    except AttributeError:
        pass
    return genre_list


def find_summary(congee):
    summary_container = congee.find_all("span", class_="sc-35061649-0 fjlUgo")
    if len(summary_container) > 0:
        summary = summary_container[0].string
    else:
        summary = "N/A"
    return summary


def find_rating(congee):
    rating_container = congee.find_all("span", class_="sc-e457ee34-1 squoh")
    if len(rating_container) > 0:
        rating = rating_container[0].string
    else:
        rating = "0"
    return rating


def get_res_dict(rating, release_date, num_reviews, genre_list, summary):
    res = {"rating": float(rating)}
    res["release_date"] = release_date
    res["num_reviews"] = num_reviews
    res["genres"] = genre_list
    res["summary"] = summary
    return res


def get_num_reviews(broth):
    header_container = broth.find_all("div", class_="header")
    num_review_indexed = header_container[0]
    num_reviews = int(
        num_review_indexed.select("div span")[0].text.split(" ")[0].replace(",", "")
    )
    return num_reviews


def check_file_existence(file_name):
    already_exists = False
    file_name = change_title_if_required(file_name)
    for json_name in os.listdir("./imdb/imdb_movie_jsons"):
        if file_name in json_name:
            print(f"\n{file_name} data already exists!")
            already_exists = True
            break
    return already_exists


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
