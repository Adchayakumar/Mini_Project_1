# The IMDb Movie Data Analysis 2024
Webscraping the IMDB 2024 movie data using selenium and making a interactive website using streamlit .

## Problem statement:
Extracting and analysis the IMDB 2024 Movie data. Finally provide interactive visualizations and filtering functionality using Streamlit

## We Separate the problem statement Into 4 parts
 * Extract (Web Scraping) the movie information from the IMDB website
 * Clean data & Analyze the pattern
 * Inser the data into Mysql data base server for efficient query
 * Make a interactive dashboard using streamlit

# Data Extraction: Using Selenium to scrape movie details such as:
* Movie Names
* Genres
* Ratings
* Voting Counts
* Durations

# Data Organization:
* Categorizing movies genre-wise.

* Saving the data as individual CSV files for each genre.

* Merging all CSV files into a single, comprehensive dataset.


# Database Management:
Storing the combined dataset in an SQL database for efficient querying.

# Data Visualization:
* Building an interactive and user-friendly dashboard using Streamlit ,
* Providing filtering options to explore movies based on genres, ratings, and more ,
  

# Key Features:
* The MYMDB Score System balances ratings and vote counts to rank movies fairly. It prevents movies with few votes but high ratings from dominating and gives more weight to movies with many positive vote

 * Interactive filter options - you can choose movie based on Movie name, genere , ratings , voting count , duration and our favourite Mymdb Score

# Technologies Used:
* Python: Core programming language.
* Selenium: For web scraping.
* Pandas: Data manipulation and analysis.
* MySQL: Storing and managing data.
* Streamlit: Interactive dashboard and visualization.

# Example Visualizations:
* Top-rated movies by genre 
* Most popular genres based on voting counts 
* Average duration of movies by genre 

# Future Improvements:
* Adding sentiment analysis of user reviews.
* Enhancing dashboard interactivity.
* Expanding data scraping to include previous years.
