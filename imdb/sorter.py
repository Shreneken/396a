import os
import shutil

directory = "./imdb/imdb_movie_jsons"
date_movies = {}

# Sorting movies by release date
for file_name in os.listdir(directory):
    
    if "json" not in file_name:
        continue
    
    if '--' in file_name:
        file_name = file_name.replace('--','(colon)')
    
    curr_file_list = file_name.split("-")
    print(f"{curr_file_list=}")
    
    for i,e in enumerate(curr_file_list): 
        try: 
            curr_file_list[i] =  int(e) 
        except:
            continue 
    
    curr_date = [x for x in curr_file_list if isinstance(x,int) and int(x) > 1900 and int(x) < 2024]
    print(curr_date)

    if len(curr_date) == 0:
        continue

    curr_date = curr_date[0]

    if curr_date not in date_movies:
        date_movies[curr_date] = [file_name]
    else:
        date_movies[curr_date].append(file_name)

for curr_date in date_movies:
    try:
        os.mkdir(f"./imdb_movie_jsons/{curr_date}")
    except:
        continue
    for movie_name in date_movies[curr_date]:
        shutil.move(
            f"./imdb_movie_jsons/{movie_name}", f"./imdb_movie_jsons/{curr_date}"
        )
