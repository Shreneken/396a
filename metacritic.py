from requests import get
from bs4 import BeautifulSoup


headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}

movies = get('https://www.metacritic.com/browse/movies/score/metascore/all/filtered?page=0',headers = headers)

# print(movies.status_code)

checkbS = BeautifulSoup(movies.content, 'html.parser')


# print(checkbS)

container = checkbS.find_all('td', class_ = "clamp-summary-wrap")
# print(type(container))

first_movie = container[0]


print(first_movie.select('a.title h3')[0].text)
print(first_movie.select('div.clamp-score-wrap a.metascore_anchor div')[0].text)











