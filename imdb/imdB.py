from requests import get
from bs4 import BeautifulSoup
from tqdm import tqdm
from urllib.parse import urljoin
from imdb_utils import writeMovieIntoJsonFile as write
from imdb_utils import check_status_code as check2
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
        json.dump(data, all_data)

# Visit each individual movie's page
for title in tqdm(data):
    movie_page_url = "https://www.imdb.com/title/" + data[title][0]["id"] + "/"
    review_url = movie_page_url + "reviews"

    movie = get(review_url, headers=HEADERS)
    own_movie = get(movie_page_url, headers=HEADERS)
    soup1 = BeautifulSoup(movie.content, "html.parser")
    congee = BeautifulSoup(own_movie.content, "html.parser")

    # Check if reponses are okay (status.code is 200)
    if not check2(movie.status_code, own_movie.status_code):
        print("Requests went wrong!")
        break

    # Finding release date
    release_date_container = soup1.find_all("div", class_="parent")
    release_date_indexed = release_date_container[0]
    release_date = release_date_indexed.select("h3 span.nobr")[0].text.split()[0]
    release_date = release_date.split("(")[1].split(")")[0]

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

    # Finding genre
    genre_list = []
    genres = congee.select_one('div.ipc-chip-list__scroller')
    for genre in genres.contents:
        genre_list.append(genre.text)

    #Find Summary
    summary_container = congee.find_all("span", class_="sc-35061649-0 fjlUgo")
    if len(summary_container) > 0:
        summary = summary_container[0].string
    else:
        summary = "N/A"
    # Adding all attributes to res
    res = {"rating": int(data[title][1]["rating"])}
    res["release_date"] = release_date
    res["num_reviews"] = int(num_review_indexed.select("div span")[0].text.split(" ")[0])
    res["genres"] = genre_list
    res["summary"] = summary

    #Check if a particular movie is already in our folder
    try:
        with open(f"./imdb_movie_jsons/{title}-{release_date}-{director}.json", "r") as _:
            print(f"\n{title} data already exists!")
            continue
    except:
        # Collecting all reviews now
        url = (
            "https://www.imdb.com/title/"+data[title][0]['id']+"/reviews/_ajax?ref_=undefined&paginationKey={}"
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
                soup.find_all(class_="title"), soup.find_all(class_="text show-more__control")
            ):
                res[t.get_text(strip=True)]=review.get_text()
        
        #Dumping into individual json files
        write(res, title, release_date, director)
