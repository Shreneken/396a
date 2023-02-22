from requests import get
from bs4 import BeautifulSoup
from tqdm import tqdm
from json import dump

#Current data: All movies from top 250 movies list

#data format: { movie_name: [
#               { id: id_here },
#                { rating: rating_here},
#                { reviewTitle: [ordered review titles here]},
#                { reviewContent: [ordered review content here]}
#               ], ...}

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
}

#Request top 250 movies page from imdB
top_250_movies = get(
    "https://www.imdb.com/chart/top/?ref_=nv_mp_mv250", headers=headers
)
print("The Status code of request is:", top_250_movies.status_code)

data = {}

#Using HTML parser from BeautifulSoup on our request
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
    data[t].append({"reviewTitle": []})
    data[t].append({"reviewContent": []})

#Visit each individual movie's page
for title in tqdm(data):
    movie = get("https://www.imdb.com/title/" + data[title][0]["id"] + "/reviews")
    bs = BeautifulSoup(movie.content, "html.parser")
    reviews = bs.find_all("div", class_="lister-item-content")

    # Add review title and review content
    for review in reviews:
        rTitle = review.select("a.title")[0].text
        rContent = review.select("div.content div.show-more__control")[0].text

        data[title][2]["reviewTitle"].append(rTitle)
        data[title][3]["reviewContent"].append(rContent)

#Add our data into imdbData.json file
with open("imdbData.json", "w") as iData:
    dump(data, iData)

reviewData = []
rTitles = data[title][2]["reviewTitle"]
rContent = data[title][3]["reviewContent"]

for i in range(len(rTitles)):
    reviewData.append({rTitles[i]: rContent[i]})

#Add a list of dicts with review titles:content format to imdbReviews.json file
with open("imdbReviews.json", "w") as outfile:
    dump(reviewData, outfile)
