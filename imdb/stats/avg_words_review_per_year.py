import os
import json
from tqdm import tqdm

directory = "./imdb/imdb_movie_jsons"
result = {}
words_per_year = 0
reviews_per_year = 0

for dir in os.listdir(directory):

    try:
        words_per_year = 0
        reviews_per_year = 0
        for movie_file in tqdm(os.listdir(directory+'/'+dir)):
            with open(f"./imdb/imdb_movie_jsons/{dir}/{movie_file}", 'r') as each_movie:
                movie_data = json.load(each_movie)
            movie_reviews = movie_data['reviews']
            reviews_per_year += len(movie_reviews)
            review_words = 0
            for r in movie_reviews:
                review_words += len(r['content'].split(' '))
            words_per_year += review_words
        result[dir] = {
            'words': words_per_year,
            'reviews': reviews_per_year,
            'average_words_year': words_per_year/reviews_per_year 
        }
        # Count has number of movies per year
    except:
        continue

with open('./imdb/stats/avg_words_review_per_year.json', 'w') as writeHere:
    json.dump(result, writeHere)




