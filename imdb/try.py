from requests import get
from bs4 import BeautifulSoup
import json
from imdb_utils import HEADERS

# url = (
#     "https://www.imdb.com/title/tt0078788/reviews/_ajax?ref_=undefined&paginationKey={}"
# )
# key = ""

# data = {}


# for i in range(1000):
#     response = requests.get(url.format(key))
#     soup = BeautifulSoup(response.content, "html.parser")
#     # Find the pagination key
#     pagination_key = soup.find("div", class_="load-more-data")
#     if not pagination_key:
#         break
#     # Update the `key` variable in-order to scrape more reviews
#     key = pagination_key["data-key"]
#     for title, review in zip(
#         soup.find_all(class_="title"), soup.find_all(class_="text show-more__control")
#     ):
#         data[title.get_text(strip=True)]=review.get_text()
#         i+=1

# with open("trying.json","w") as trying:
#     json.dump(data,trying)


movie_page_url = "https://letterboxd.com/film/the-godfather/"

own_movie = get(movie_page_url)
congee = BeautifulSoup(own_movie.content, "html.parser")



summary_container = congee.find_all("section", class_="section ratings-histogram-chart")
print(summary_container)
summary = summary_container[0].select("h2.section-heading a")[0].text
print(summary)

# summary_container = congee.find_all("span", class_="sc-35061649-0 fjlUgo")
# summary = summary_container[0].string

# print(summary)
