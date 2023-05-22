import json
import os
from collections import Counter
import matplotlib.pyplot as plt

genres = Counter()
for movie_year in tuple(os.walk("./MergedData/merged_movie_jsons"))[0][1]:
    subdir = tuple(os.walk(f"./MergedData/merged_movie_jsons/{movie_year}"))
    for file_name in tuple(subdir)[0][-1]:
        # print(f"{subdir[0][0]}/{file_name}")
        with open(f"{subdir[0][0]}/{file_name}", 'r', encoding="utf-8") as f:
            file = json.load(f)

        try:
            genres.update(file["genres"])
        except:
            pass

with open(f"./MergedData/stats/genres.json", 'w', encoding="utf-8") as wr:
    json.dump(genres, wr, indent=4)

