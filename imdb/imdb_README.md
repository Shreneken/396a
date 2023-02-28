
# Scraping IMDB 

## Current data: All movies from top 250 movies list

#### data format for each `movieName_releaseData_Director.json`:
               {
                { rating: rating_here},
                { release_data: release_date_here}.
                { num_reviews: number_of_reviews_here},
                { reviewTitle: reviewContent} for each review title and content
               }


#### Getting movie data 
  - Run `./run_py_scripts.sh` in your terminal while under the `imdb` directory. If running from Windows, use `Git Bash`, WSL or any other alternative for bash shell 

    OR

  - Run `imdb.py` which will add `movieName_releaseData_Director.json` for each movie inside the `imdb_movie_jsons` directory
  - Then run `sorter.py` to categorize the `movieName_releaseData_Director.json` files into different directors sorted by release date.

  - `imdb.py` will also create a `imdBData.json` if it does not already exist. This file contains data in top250 movies list form imdB.


- Checkout `imdb_utils.py` for any helper functions.
