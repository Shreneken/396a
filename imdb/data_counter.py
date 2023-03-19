import os
import json

directory = "./imdb/imdb_movie_jsons"

count = {}
total_count = 0
outsider = 0

for dir in os.listdir(directory):

    try:
        dir_count = 0
        for movie_file in os.listdir(directory+'/'+dir):
            dir_count +=1
            total_count+=1
        count[dir] = dir_count
        print(f"count for {str(dir)} is {dir_count}")
    except:
        total_count+=1
        outsider += 1
        continue

with open('./imdb/movie_count_for_date.json', 'w') as movie_count:
    json.dump(count, movie_count)

sumVal = sum(count.values())

print(f'{total_count} - {sumVal} - {outsider} - {total_count - sumVal}')