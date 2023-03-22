# Movie Data Getter

Scraping movie websites for data!

### data format for each `"movie_name-release_date-Director_name".json`:
 ```js
   {
      rating: rating_here,
      release_date: release_date_here,
      num_reviews: number_of_reviews_here,
      genre : [genre_here],
      summary: summary_here,
      reviews: [reviewContent] 
   }

   //each reviewContent obj format:
   {
    review_title: review_title
    content: review_content
    review_date: review_date_here
   }
 ```

### Directory Structure:
    source -> 
    source_movie_jsons -> 
    dir for all release dates -> 
    corresponding movies
