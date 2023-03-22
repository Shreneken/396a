from requests import get
from bs4 import BeautifulSoup
from datetime import datetime
import calendar
import os
import json
f = open("Metacritic/file_err_log.json")
movie_list = json.load(f)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
ERROR_FILE = "Metacritic/file_err_log.json"


def __get_param(movie_name: str):
    """convert the movie into a url format with metacritic url format"""
    symbols_to_remove = {".", "'", ",", ":", "&", "(", ")"}
    symbols_to_replace = {" "}
    param_char = []
    for letter in movie_name:
        if letter in symbols_to_remove:
            letter = ""
        elif letter in symbols_to_replace:
            letter = "-"
        param_char.append(letter.lower())
    return "".join(param_char).replace("--", "-")


def __get_url(movie_name: str):
    param = __get_param(movie_name)
    return f"https://www.metacritic.com/movie/{param}/"


def fetch(movie_name: str):
    url = __get_url(movie_name)
    return get(url, headers=HEADERS)


def get_rating(bs_obj):
    rating = bs_obj.find("span", class_="user").text.strip()
    try:
        rating = float(rating)
    except ValueError:
        pass
    return rating


def get_date_format(date):
    months = {'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
              'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12}
    date_arr = date.text.strip().replace("  ", " ").split(" ")[:3]
    # if month is in short form, convert it to full form
    if date_arr[0].lower() in months:
        date_arr[0] = calendar.month_name[months[date_arr[0].lower()]]
    date_str = " ".join(date_arr)
    datetime_object = datetime.strptime(date_str, '%B %d, %Y')
    return str(datetime_object.date())


def get_release_date(bs_obj):
    container = bs_obj.find("span", class_="release_date")
    try:
        date = container.find_all("span", class_="")[0]
        release_date = get_date_format(date)
    except:
        release_date = container.find_all("span", class_="")[0].text
    return release_date


def get_genre(bs_obj):
    movie_content = bs_obj.find_all("div", class_="genres")
    genres = movie_content[0].select("span")[1].text.strip().split(",")
    genres = [genre.strip() for genre in genres]
    return genres


def get_summary(bs_obj):
    container = bs_obj.find("div", class_="summary_deck")
    return container.find_all("span", class_="")[0].text.strip()


def get_critic_reviews(movie_name):
    url = __get_url(movie_name) + r"critic-reviews"
    web_page = get(url, headers=HEADERS)
    bs_reviews = BeautifulSoup(web_page.content, "html.parser")
    reviews_content = bs_reviews.find_all("a", class_="no_hover")
    return [review.text.strip() for review in reviews_content]


def get_user_reviews(movie_name):
    user_review_link = __get_url(movie_name) + r"user-reviews"
    web_page = get(user_review_link, headers=HEADERS)
    bs_reviews = BeautifulSoup(web_page.content, "html.parser")
    reviews = bs_reviews.find_all("div", class_="review")
    result = []
    for review in reviews:
        content = {
            "review_title": None,
            "content": review.find("div", class_="review_body").text.strip().replace("… Expand", ""),
            "review_date": get_date_format(review.find("span", class_="date"))
        }
        result.append(content)
    return result


def get_director(bs_obj):
    return bs_obj.find("div", class_="director").find("a").text


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


def get_file_name(movie_name, release_date, director):
    directory = create_dir(release_date)
    file_name = f"{movie_name}-{release_date}-{director}.json"
    return directory + change_title_if_required(file_name)


def create_dir(release_date):
    """create the directory for the year if it does not exist
        a "miscellaneous" directory is created if the year can not be detected"""
    dir_to_check = release_date.split("-")[0]
    try:
        int(dir_to_check)
        dir_to_check = "Metacritic/metacritic_movies_json/" + dir_to_check + "/"
    except ValueError:
        dir_to_check = "Metacritic/metacritic_movies_json/" + "miscellaneous/"
    if not os.path.exists(dir_to_check):
        os.makedirs(dir_to_check)
    return dir_to_check

error_logs = {}
for i, movie in enumerate(movie_list):
    try:
        web_page = fetch(movie)
    except:
        error_logs[movie] = "unable to find movie webpage\n"
        continue
    bs = BeautifulSoup(web_page.content, 'html.parser')
    data = {}
    try:
        data["title"] = movie
    except:
        error_logs[movie] = "unable to find movie title\n"
        continue
    try:
        data["rating"] = get_rating(bs)
    except:
        error_logs[movie] = "unable to find movie rating\n"
        continue
    try:
        data["release_date"] = get_release_date(bs)
    except:
        error_logs[movie] = "unable to find or standardize release date\n"
        continue
    try:
        data["genre"] = get_genre(bs)
    except:
        error_logs[movie] = "unable to find movie genre\n"
        continue
    try:
        data["summary"] = get_summary(bs)
    except:
        error_logs[movie] = "unable to find movie summary\n"
        continue
    try:
        data["critic_reviews"] = get_critic_reviews(movie)
    except:
        error_logs[movie] = "unable to find critic review\n"
        continue
    try:
        data["reviews"] = get_user_reviews(movie)
    except:
        error_logs[movie] = "unable to find movie reviews\n"
        continue
    try:
        data["num_reviews"] = len(
            data["critic_reviews"]) + len(data["reviews"])
    except:
        error_logs[movie] = "unable to compute number of reviews\n"
        continue
    try:
        filename = get_file_name(movie, data["release_date"], get_director(bs))
        with open(filename, "w", encoding="utf-8") as dataset_json:
            json.dump(data, dataset_json,  indent=2, ensure_ascii=False)
        print(f"{i}: done with {movie}")
    except:
        error_logs[movie] = "unable to create file for the movie\n"
        continue

with open(ERROR_FILE, "w", encoding="utf-8") as log_error:
    json.dump(error_logs, log_error, indent=2)