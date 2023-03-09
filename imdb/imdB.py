from requests import get
from bs4 import BeautifulSoup
from tqdm import tqdm
import imdb_utils
import json
from datetime import datetime

HEADERS = imdb_utils.HEADERS
with open("./imdb/movie_title-id.json", "r") as movie_title_list:
    data = json.load(movie_title_list)

# Visit each individual movie's page
for title in tqdm(data):

    # Check if file already exists
    already_exists = imdb_utils.check_file_existence(title)
    if already_exists:
        continue

    movie_page_url = "https://www.imdb.com/title/tt" + data[title] + "/"
    review_url = movie_page_url + "reviews"
    movie = get(review_url, headers=HEADERS)
    own_movie = get(movie_page_url, headers=HEADERS)
    broth = BeautifulSoup(movie.content, "lxml")
    congee = BeautifulSoup(own_movie.content, "lxml")

    # Check if reponses are okay (status.code is 200)
    if not imdb_utils.check_status_code(movie.status_code, own_movie.status_code):
        print("Requests went wrong!")
        break

    # Finding number of reviews
    num_reviews = imdb_utils.get_num_reviews(broth)

    # Finding director
    director = imdb_utils.find_director(congee)

    # Finding release date
    release_date = imdb_utils.find_release_date(congee)

    # Finding genre
    genre_list = imdb_utils.find_genre(congee)

    # Find Summary
    summary = imdb_utils.find_summary(congee)

    # Find rating
    rating = imdb_utils.find_rating(congee)

    # Adding all attributes to res
    res = imdb_utils.get_res_dict(
        rating, release_date, num_reviews, genre_list, summary
    )

    res["reviews"] = []

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
        for t, review, review_date in zip(
            soup.find_all(class_="title"),
            soup.find_all(class_="text show-more__control"),
            soup.find_all(class_="review-date"),
        ):
            res["reviews"].append(
                {
                    "review_title": t.get_text(strip=True),
                    "content": review.get_text(),
                    "review_date": str(datetime.strptime(review_date.get_text(strip=True),"%d %B %Y").date())
                }
            )

    title = imdb_utils.change_title_if_required(title)

    # Dumping into individual json files
    imdb_utils.writeMovieIntoJsonFile(res, title, release_date, director)
