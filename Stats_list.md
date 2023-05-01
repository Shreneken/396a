- Total Number of tokens
- Average tokens per movie per year(release date)
- Total tokens per year
- Average tokens per movie as a whole
- Highest and lowest tokens per movie
- Number of movies rated < 7.0
- Number of movies rated >= 7.0
- Number of tokens and reviews for < 7.0 rating
- Number of tokens and reviews for > 7.0 rating
- Number of tokens and reviews per genre ( movies with multiple genres will get put into  all genres)
- Links between genres and vibes (after we get vibes) (eg. horror - thrilling: sankey chart)
- idea: Histogram to bucket words-review, rating-reviews
- Box-plot for visualization
- Links between ratings and vibes (after we get vibes)
- Number of movies per year (correlation between how many movies to year to analyze recency bias) bar chart
- Source of list of movies (top 1000 most popular movies and 250 least popular movies on imdb on 2nd March 2023) - (https://www.imdb.com/search/title/?groups=top_1000)
- Number of tokens(words) with a specific length range (1 - 10…)




Motivation, Composition, Collection Process, Cleaning, Maintenance

Composition
Choosing the list of movies and the exact raw data collected (reviews, ratings, summary, etc.)
Final instances: list of movies with corresponding vibes
List of vibes found and the number of movies associated with each one (potentially list of the movies)
The sources we used and the date we retrieved our data from → not self-contained and data will become irrelevant pretty soon
The data is not confidential (publicly available) and no individual user can be identified using it.
Does the dataset contain any sensitive information?
- Effort to remove these (including profanity/disturbing info)

Collection Process
- What techniques did we use to collect movie ratings? (beautiful soup, web scraping)
- Who was involved in the data collection process? (just us, no crowdworkers)
- Individuals consent to their data being used

Preprocessing/cleaning/labeling
- How was the data preprocessed (tokenization, tf-idf, python, model that gave us the vibes)
- Was the raw data saved for future work?
- How were the vibes extracted from the movie ratings?
- Link to repository
- What could the dataset be used for?

Distribution
- How will the dataset be made available? (API, GitHub?)
- 3rd Parties licensing (imdb, rt, metacritic)

Maintenence
- Contacting the owner
- Who will be hosting the dataset
