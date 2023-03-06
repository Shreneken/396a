# from requests import get
# from bs4 import BeautifulSoup
# import json
# from imdb_utils import HEADERS
# from datetime import datetime


# # # url = (
# # #     "https://www.imdb.com/title/tt0078788/reviews/_ajax?ref_=undefined&paginationKey={}"
# # # )
# # # key = ""

# # # data = {}


# # # for i in range(1000):
# # #     response = requests.get(url.format(key))
# # #     soup = BeautifulSoup(response.content, "html.parser")
# # #     # Find the pagination key
# # #     pagination_key = soup.find("div", class_="load-more-data")
# # #     if not pagination_key:
# # #         break
# # #     # Update the `key` variable in-order to scrape more reviews
# # #     key = pagination_key["data-key"]
# # #     for title, review in zip(
# # #         soup.find_all(class_="title"), soup.find_all(class_="text show-more__control")
# # #     ):
# # #         data[title.get_text(strip=True)]=review.get_text()
# # #         i+=1

# # # with open("trying.json","w") as trying:
# # #     json.dump(data,trying)


# movie_page_url = "https://www.imdb.com/title/tt0111160/"

# own_movie = get(movie_page_url, headers=HEADERS)

# print(f"{own_movie.status_code=}")
# congee = BeautifulSoup(own_movie.content, "lxml")

# release_date_container = congee.find_all(
#     "ul",
#     class_="ipc-metadata-list ipc-metadata-list--dividers-all ipc-metadata-list--base",
# )
# release_date_indexed = release_date_container[0]
# release_date_arr = release_date_indexed.select("li div ul li a")[0].text
# print(f"{release_date_arr=}")
# # summary_container = congee.find_all("section", class_="section ratings-histogram-chart")
# # print(summary_container)
# # summary = summary_container[0].select("h2.section-heading a")[0].text
# # print(summary)

# # # summary_container = congee.find_all("span", class_="sc-35061649-0 fjlUgo")
# # # summary = summary_container[0].string

# # # print(summary)

# # date_str = "19 April, 2002"
# # datetime_object = datetime.strptime(date_str,'%d %B, %Y')

# # print(datetime_object)

 
class cope:
    def __init__(self):
     self.value = "Hello"
    
    def __repr__(self):
      return self.value
  
coper = cope()
print(coper)