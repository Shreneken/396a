# Movie Data Getter

Scraping movie websites for data and gettting vibes for them!

### Merged data with associated vibes can be found in `MergedData`

### Final format for each `movieName_releaseData_Director.json`:
 ```js
   {
      rating: rating_here,
      release_data: release_date_here,
      num_reviews: number_of_reviews_here,
      genre : [genre_here],
      summary: summary_here,
      reviews: [reviewContent],
      vibes : [corresponding_vibes],
      rt_rating: rating_from_RottenTomates_here,
      rt_summary: summary_from_RottenTomates_here,
      meta_rating: rating_from_Metacritic_here,
      meta_summary: summary_from_Metacritic_here
   }

   //each reviewContent obj format:
   {
    review_title: review_title
    content: review_content
    review_date: review_date_here
    lang: language_for_review - cleaned to only include en(english) reviews
    source: source_for_view
   }
 ```

### Directory Structure:

#### For source directories (imdb, RottenTomatoes, Metacritic, MergedData):
    source -> 
    source_movie_jsons -> 
      dir for all release year | miscellaneous -> corresponding movies
    stats ->
      figures | jsons including statistics
    scripts used for collection/tagging/cleaning
#### For Utilities:
    -> scripts used to extract figures and run extraction (tf-idf):

  
Bad_reviews.txt: irregular reviews cleaned from dataset

stopwords.json: words removed in pipeline

