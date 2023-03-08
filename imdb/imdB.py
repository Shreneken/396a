from datetime import datetime
from requests import get
from bs4 import BeautifulSoup
from tqdm import tqdm
from urllib.parse import urljoin
from imdb_utils import writeMovieIntoJsonFile as write
from imdb_utils import check_status_code as check2
from imdb_utils import check as check1
from imdb_utils import getData
from imdb_utils import HEADERS
import json
import os

with open("./imdb/movie_title-id.json", "r") as movie_title_list:
    data = json.load(movie_title_list)

# Visit each individual movie's page
for title in tqdm(data):

    file_name = title
    already_exists = False
    if ":" in title:
        file_name = "--".join(title.split(":"))
    for json_name in os.listdir("./imdb/imdb_movie_jsons"):
        if file_name in json_name:
            print(f"\n{title} data already exists!")
            already_exists = True
            break
    if already_exists:
        continue
    movie_page_url = "https://www.imdb.com/title/tt" + data[title] + "/"
    review_url = movie_page_url + "reviews"
    movie = get(review_url, headers=HEADERS)
    own_movie = get(movie_page_url, headers=HEADERS)
    soup1 = BeautifulSoup(movie.content, "lxml")
    congee = BeautifulSoup(own_movie.content, "lxml")

    # Check if reponses are okay (status.code is 200)
    if not check2(movie.status_code, own_movie.status_code):
        print("Requests went wrong!")
        break

    # Finding number of reviews
    header_container = soup1.find_all("div", class_="header")
    num_review_indexed = header_container[0]

    # Finding director
    director_container = congee.find_all(
        "a",
        class_="ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link",
    )
    director_indexed = director_container[0]
    director = director_indexed.string

    # Finding release date using director container
    release_date_container = congee.find_all(
        "ul",
        class_="ipc-metadata-list ipc-metadata-list--dividers-all ipc-metadata-list--base",
    )
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
    release_date_str = " ".join(release_date_arr)
    datetime_object = datetime.strptime(release_date_str, "%B %d, %Y")
    release_date = str(datetime_object.date())

    # Finding genre
    genre_list = []
    genres = congee.select_one("div.ipc-chip-list__scroller")
    for genre in genres.contents:
        genre_list.append(genre.text)

    # Find Summary
    summary_container = congee.find_all("span", class_="sc-35061649-0 fjlUgo")
    if len(summary_container) > 0:
        summary = summary_container[0].string
    else:
        summary = "N/A"

    # Find rating
    rating_container = congee.find_all("span", class_="sc-e457ee34-1 squoh")
    if len(rating_container) > 0:
        rating = rating_container[0].string
    else:
        rating = "0"

    # Adding all attributes to res
    res = {"rating": float(rating)}
    res["release_date"] = release_date
    res["num_reviews"] = int(
        num_review_indexed.select("div span")[0].text.split(" ")[0].replace(",", "")
    )
    res["genres"] = genre_list
    res["summary"] = summary

    # Check if a particular movie is already in our folder

    # Collecting all reviews now
    url = (
        "https://www.imdb.com/title/tt"
        + data[title]
        + "/reviews/_ajax?ref_=undefined&paginationKey={}"
    )
    key = ""

    for i in range(1000):
        response = get(url.format(key))
        soup = BeautifulSoup(response.content, "html.parser")
        # Find the pagination key
        pagination_key = soup.find("div", class_="load-more-data")
        if not pagination_key:
            break
        # Update the `key` variable in-order to scrape more reviews
        key = pagination_key["data-key"]
        for t, review in zip(
            soup.find_all(class_="title"),
            soup.find_all(class_="text show-more__control"),
        ):
            res[t.get_text(strip=True)] = review.get_text()

    if ":" in title:
        title = "--".join(title.split(":"))
    # Dumping into individual json files
    write(res, title, release_date, director)
