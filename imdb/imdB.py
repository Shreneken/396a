from requests import get
from bs4 import BeautifulSoup
from tqdm import tqdm
from urllib.parse import urljoin
from imdb_utils import writeMovieIntoJsonFile as write
from imdb_utils import check_status_code as check3
from imdb_utils import check as check1
from imdb_utils import loadJSONintoDict as load_dict
from imdb_utils import getData
from imdb_utils import HEADERS
import json


try:
    data = load_dict("./imdbData.json")
    print("We already have data!")
except:
    print("We need to get data again!")
    data = getData()
    with open("./imdbData.json", "w") as all_data:
        json.dump(data, all_data, indent=4, sort_keys=True)

# Visit each individual movie's page
for title in tqdm(data):
    movie_page_url = "https://www.imdb.com/title/" + data[title][0]["id"] + "/"
    review_url = movie_page_url + "reviews"
    own_url = movie_page_url + "?ref_=tt_urv"

    movie = get(review_url, headers=HEADERS)
    own_movie = get(own_url, headers=HEADERS)
    soup = BeautifulSoup(movie.content, "html.parser")
    main_content = urljoin(
        review_url, soup.select(".load-more-data")[0]["data-ajaxurl"]
    )  # extracting the link leading to the page containing everything available here
    loadMore_reviews = get(main_content, headers=HEADERS)
    broth = BeautifulSoup(loadMore_reviews.content, "html.parser")
    congee = BeautifulSoup(own_movie.content, "html.parser")

    # Check if all reponses are okay (status.code is 200)
    if not check3(
        movie.status_code, own_movie.status_code, loadMore_reviews.status_code
    ):
        print("Requests went wrong!")
        break

    # Finding release date
    release_date_container = soup.find_all("div", class_="parent")
    release_date_indexed = release_date_container[0]
    release_date = release_date_indexed.select("h3 span.nobr")[0].text.split()[0]
    release_date = release_date.split("(")[1].split(")")[0]

    # Finding number of reviews
    header_container = soup.find_all("div", class_="header")
    num_review_indexed = header_container[0]

    # Finding director
    director_container = congee.find_all(
        "a",
        class_="ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link",
    )
    director_indexed = director_container[0]
    director = director_indexed.string

    # Adding all attributes to res
    res = {"rating": data[title][1]["rating"]}
    res["release_date"] = release_date
    res["num_reviews"] = num_review_indexed.select("div span")[0].text
    res["director"] = director

    for item in broth.select(".review-container"):
        rt = item.select(".title")[0].text
        review = item.select(".text")[0].text
        res[rt] = review

    write(res, title, release_date, director)
