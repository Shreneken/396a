import json
import os


files = []
# Metacritic/metacritic_movies_json
for movie_year in tuple(os.walk("./Metacritic/metacritic_movies_json"))[0][1]:
    subdir = tuple(os.walk(f"./Metacritic/metacritic_movies_json/{movie_year}"))
    for file_name in tuple(subdir)[0][-1]:
        # print(f"{subdir[0][0]}/{file_name}")
        with open(f"{subdir[0][0]}/{file_name}", 'r', encoding="utf-8") as f:
            data = json.load(f)
        
        data["genres"] = data["genre"]
        del data["genre"]

        with open(f"{subdir[0][0]}/{file_name}", "w", encoding="utf-8") as dataset_json:
            json.dump(data, dataset_json,  indent=2, ensure_ascii=False)
