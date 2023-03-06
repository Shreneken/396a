import imdb
import json
from tqdm import tqdm

ia = imdb.IMDb()

DATA_NEEDED = False

with open("./imdb/movie_title-id.json", "r") as data:
    current_data = json.load(data)

with open('./movie_titles_list.json', "r") as movie_list:
    movies = json.load(movie_list)

if DATA_NEEDED:
    for i in tqdm(range(0, len(movies))):
        # searching the name
        name = movies[i]
        try:
            search = ia.search_movie(name)
            # getting the id
            id = search[0].movieID
            current_data[name]=[id]
        except Exception:
            continue


for movie_name in current_data:
    if len(current_data[movie_name]) > 0:
        current_data[movie_name] = current_data[movie_name][0]

with open("./imdB/movie_title-id.json", "w") as data_list:
    json.dump(current_data, data_list)

