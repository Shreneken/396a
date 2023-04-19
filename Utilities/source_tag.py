import os
import json
from tqdm import tqdm

def tag_reviews(dir_name, source):
    for date_dir in os.listdir(dir_name):
        new_dir = f"{dir_name}/{date_dir}/"
        try:
            for each_movie in tqdm(os.listdir(new_dir)):
                try:
                    movie_file = f"{new_dir}/{each_movie}"
                    with open(movie_file, "r+") as read_movie:
                        load_curr_movie = json.load(read_movie)
                        for review in load_curr_movie["reviews"]:
                            review['source'] = source
                    with open(movie_file, "w", encoding="utf-8") as dataset_json:
                        json.dump(load_curr_movie, dataset_json,  indent=2, ensure_ascii=False)
                except Exception:
                    print("Skipping to next movie in dir ", each_movie)
                    continue
        except Exception:
            print("Skipping to next dir ", dir_name)
            continue

if __name__ == "__main__":
    tag_reviews("Metacritic/metacritic_movies_json", "metacritic")