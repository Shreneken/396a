from langdetect import detect_langs
import os
import json
from tqdm import tqdm

for date_dir in os.listdir("./imdb/imdb_movie_jsons"):
    new_dir = f"./imdb/imdb_movie_jsons/{date_dir}/"
    if int(date_dir) != 2018:
        continue
    try:
        for each_movie in tqdm(os.listdir(new_dir)):
            try:
                file = f"./imdb/imdb_movie_jsons/{date_dir}/{each_movie}"

                with open(file, "r+") as read_movie:
                    load_curr_movie = json.load(read_movie)
                    for review in load_curr_movie["reviews"]:
                        content = review["content"]
                        lang_prob = detect_langs(content)
                        languages = [x.lang for x in lang_prob if x.prob > 0.7]
                        if len(languages) > 0 and languages[0] == "en":
                            review["lang"] = languages[0]
                        else:
                            continue
                    load_curr_movie["reviews"] = [
                        review
                        for review in load_curr_movie["reviews"]
                        if review["lang"] == "en"
                    ]
                with open(file, "w") as write_to_movie:
                    json.dump(load_curr_movie, write_to_movie, indent=4)
                    # print(load_curr_movie)
            except:
                print("Skipping to next movie in dir")
                continue
    except:
        print("Skipping to next dir")
        continue
