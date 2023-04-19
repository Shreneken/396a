# Movie Data Getter

Scraping movie websites for data!

### data format for each `movieName_releaseData_Director.json`:
 ```js
   {
      rating: rating_here,
      release_data: release_date_here,
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
    dir for all release year | miscellaneous -> 
    corresponding movies
length by tokens, average tokens per review, number of reviews

mindful of other laguages
patterns for data
