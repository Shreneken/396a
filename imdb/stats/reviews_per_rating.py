import math
import os
import json
from tqdm import tqdm

directory = "./imdb/imdb_movie_jsons"
result = {x:{'words_per_rating':0, 'reviews_per_rating':0} for x in range(1,11)}

for dir in os.listdir(directory):
    try:
        for movie_file in tqdm(os.listdir(directory+'/'+dir)):
            with open(f"./imdb/imdb_movie_jsons/{dir}/{movie_file}", 'r') as each_movie:
                movie_data = json.load(each_movie)
            movie_reviews = movie_data['reviews']
            curr_rating = math.floor(movie_data['rating'])
            result[curr_rating]['reviews_per_rating'] += len(movie_reviews)
            review_words = 0
            for r in movie_reviews:
                review_words += len(r['content'].split(' '))
            result[curr_rating]['words_per_rating'] += review_words
    except:
        continue

for date in result:
    try:
        result[date]['avg'] = result[date]['words_per_rating']/result[date]['reviews_per_rating']
    except:
        continue
    
with open('./imdb/stats/reviews_per_rating.json', 'w') as writeHere:
    json.dump(result, writeHere)




