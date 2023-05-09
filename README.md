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

TODO:
- look at jq to query json data
- Think about if you need a set of vibes to match it or leave it open ended
- wordnet (its a network of words that has how things are related to each other, including synonyms)
- How do you know which keywords extracted are vibes?


- look at extraction of vibes on a subset of reviews 
- get everything, merge 
- iteratively clean (tokenizing, lower casing, look at what spaCy can detect)

Limitations: Non-Obvious, limitation of algorithm, only-english reviews, only popular movies, effect quality or diversity of data (would effect ppl using it)  

5/3 
TODO:
- Proceed to try tf-idf:
  - decide on a final result format
  - utilize save funciton in gensum
- otherwise, try topic modeling
