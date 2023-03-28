import os
import json
from tqdm import tqdm


directory = "./imdb/imdb_movie_jsons"

count = {}
movie_count = 0
review_count = 0
outsider = 0
result = []
total_words = 0

for dir in os.listdir(directory):

    try:
        dir_count = 0
        for movie_file in tqdm(os.listdir(directory+'/'+dir)):
            dir_count +=1
            movie_count+=1
            with open(f"./imdb/imdb_movie_jsons/{dir}/{movie_file}", 'r') as each_movie:
                movie_data = json.load(each_movie)
            movie_reviews = movie_data['reviews']
            num_reviews = len(movie_reviews)
            review_count += num_reviews
            review_words = 0
            for r in movie_reviews:
                review_words += len(r['content'].split(' '))
            total_words += review_words
            avg_words = review_words/num_reviews
            result.append( {movie_file: [
                {f'Number of reviews for {movie_file}': num_reviews},
                {f'Number of words for {movie_file}': review_words},
                {f'Average word per review for {movie_file}': avg_words}
            ]})
        count[dir] = dir_count
        # Count has number of movies per year
    except:
        movie_count+=1
        outsider += 1
        continue

result.append( {"Total number of reviews" : review_count})
result.append( {'Total number of words': total_words})
result.append( {'Average words per review': total_words/review_count})
result.append( {"Movies per Year" : count})



with open('./imdb/imdb_stats.json', 'w') as writeHere:
    json.dump(result, writeHere)




