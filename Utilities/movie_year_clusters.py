import os
import json

def get_yearly_movie_count(dir_name: str, output_filename: str, year_group: int = 10) -> None:
    """
    writes the number of movies for each tear to a file in json format
    Parameters
    ----------
    dir_name: str
        the parent directory containing directories whose names are years eg Metacritic/metacritic_movies_json/2020
        standard:: {source}/{source}_movies_json/{year}

    output_filename: str
        the file where the output json would be stored
    year_group: int {optional}, default = 10
        defines the desired ranges eg. (1 - 10, 11 - 20) had year_group = 10
    """
    if not os.path.isdir(dir_name):
        print(f"{dir_name} is not a directory")
        raise NotADirectoryError()

    years = {} # {year: number_of_movies}
    subdir = tuple(os.walk(dir_name))
    for i, movie_year_dir in enumerate(sorted(subdir[1:])):
        movie_year = os.path.basename(movie_year_dir[0])
        try:
            movie_year = int(movie_year)
        except ValueError:
            pass
        years[movie_year] =len(movie_year_dir[2])
    
    bucket = {} #{year_start - year_end: num_movies}
    if(year_group < 0):
        raise ZeroDivisionError
    for year, num_movies in years.items():
        if isinstance(year, int):
            bucket[year//year_group] = bucket.get(year//year_group, 0) + num_movies
        else:
            bucket[year] = bucket.get(year, 0) + num_movies
    
    # adjust key value to reflect ranges
    json_output = {}
    for bucket_year in bucket.keys():
        if isinstance(bucket_year, int):
            start_year = bucket_year * year_group
            end_year = start_year + year_group - 1
            json_output[f"{start_year} - {end_year}"] = bucket[bucket_year]
        else:
            json_output[f"{bucket_year}"] = bucket[bucket_year]

    with open(output_filename, "w", encoding="utf-8") as movie_year_stats:
        json.dump(json_output, movie_year_stats,  indent=2, ensure_ascii=False)


if __name__ == "__main__":
    # dir_name = "imdb/imdb_movie_jsons/"
    # output_file = "imdb/stats/year_clusters.json"
    # get_yearly_movie_count(dir_name, output_file)
    dir_name = "MergedData/merged_movie_jsons"
    output_file = "MergedData/merged_movie_jsons"
    get_yearly_movie_count(dir_name, output_file)
