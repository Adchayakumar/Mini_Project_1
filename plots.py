import atexit
import streamlit as st
import pandas as pd
import pymysql
import seaborn as sns
import matplotlib.pyplot as plt
import connect  #this file have the Data base connection details
conn=connect.connect_db()
from scroller import info_plates  #Html content for info plates



# fetch the data from Data base for show the interactive top rated movies by genre
@st.cache_data #cache the return data of funtion 
def fetched_data(base_query):
    with conn.cursor() as cursor:
        cursor.execute(base_query)
        return cursor.fetchall()

#fetch the data from data base and return the DataFrame for ploting
@st.cache_data 
def fetch_data(query, columns):

    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=columns)
    return df

# Plot: Rating Distribution (Boxplot)
@st.cache_data
def plot_rating_distribution():
    df = fetch_data("SELECT ratings FROM movie_list", columns=["ratings"]) #make the datadframe using fetch_data()
    
    fig, ax = plt.subplots(1,  figsize=(13, 8))  #make a space for plot and fix a size of 13x8
    sns.boxplot(data=df, x='ratings', ax=ax)
    ax.set_title("Boxplot of Movie Ratings",fontsize=24, fontweight='bold', fontfamily='serif', color='teal')
    ax.set_xticks(range(1, 11))  # fix the range of ticks to 10 so numbers come like 1,2,3...10
    ax.set_xticklabels(range(1, 11)) 
    ax.set_xlabel("Movie Ratings", fontsize=18, fontweight='bold', fontfamily='serif', color='teal')
    ax.set_ylabel("Frequency", fontsize=18, fontweight='bold', fontfamily='serif', color='teal')
    ax.tick_params(axis='both', labelsize=12)  # Change tick labels font size
    st.pyplot(fig)
   
    # insights for box plots manually enterd value
    st.write("""### 🌟 **Key Insights from the Movie Ratings Boxplot** 🌟  
    - **Most movies are liked:** Ratings are mainly between **5 and 7**, showing that viewers generally have a **positive opinion**.  
    - **A few love or hate extremes:** Some movies received **very low (1–3)** or **very high (9–10)** ratings, but these are **rare cases**.  
    - **Overall positive trend:** The distribution leans slightly towards **higher ratings**, suggesting an **overall good impression** from viewers.""")




# Plot: Most Popular Genres by Voting (Pie Chart)
@st.cache_data
def plot_popular_genres():
    # Fetch data
    df = fetch_data(
        "SELECT g.genre_name, SUM(ml.votings) as total_votes FROM movie_list ml JOIN genres g ON ml.genre_id = g.genre_id GROUP BY g.genre_name",
        columns=["genre_name", "total_votes"]
    )
    
    # Sort genres by votes in descending order
    df = df.sort_values(by='total_votes', ascending=False).reset_index(drop=True)
    
    # Select top 15 genres
    top_genres = df[:12]
    
    # Combine remaining genres as 'Others'
    others_votes = df[12:]['total_votes'].sum()
    others_row = pd.DataFrame({'genre_name': ['Others'], 'total_votes': [others_votes]})
    
    # Concatenate top 15 genres with 'Others'
    df_top = pd.concat([top_genres, others_row], ignore_index=True)
    
    # Create pie chart
    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(
        df_top['total_votes'],
        labels=df_top['genre_name'],
        autopct='%1.1f%%',
        startangle=90,
        textprops={'fontsize': 10},
        wedgeprops={'linewidth': 1, 'edgecolor': 'white'},
        rotatelabels=True
    )
    
    # Improve readability of percentage labels
    for text in texts:
        text.set_fontsize(8)
    for autotext in autotexts:
        autotext.set_rotation(0)
        autotext.set_fontsize(8)
        autotext.set_color('black')
    
    # Set title
    ax.set_title("Top Popular Genres by Voting", fontsize=15)
    st.pyplot(fig)
    st.write("""- 🎬 **Action** leads with **13.3%** of the votes, making it the most popular genre, followed closely by **Thriller (12.2%)** and **Drama (10.5%)**.  
             - 😎 **Adventure and Comedy** also stand strong, each grabbing around **10%** of the votes, showing a balanced audience preference.  
        - 🌀 The **"Others"** category, representing **13 genres**, contributes **8.9%** of the votes, indicating a diverse but less dominant interest in niche genres.  
                            """)






# 4️⃣ Plot: Duration Extremes
@st.cache_data
def plot_duration_extremes():
    # Updated SQL query with the new columns and JOIN
    query = """
    SELECT ml.movie_name, ml.ratings, ml.votings, ml.duration, ml.score, g.genre_name
    FROM movie_list ml
    JOIN genres g ON ml.genre_id = g.genre_id
    """
    
    # Fetch data with column names
    df = fetch_data(query, columns=["movie_name", "rating", "votes", "duration", "score", "genre"])

    # Find shortest and longest movies
    shortest = df.nsmallest(1, 'duration').iloc[0]
    longest = df.nlargest(1, 'duration').iloc[0]

    # HTML template for info plates
    info_plate_template = """
    <div class="info-plate">
        <div class="movie-name">{movie_name}</div>
        <div class="details-row">
            <span class="detail-item" data-tooltip="Movie Rating">
                <i class="fas fa-film"></i> Rating: {rating}
            </span>
            <span class="detail-item" data-tooltip="Duration">
                <i class="fas fa-clock"></i> {duration} min
            </span>
            <span class="detail-item" data-tooltip="MYMDb Score">
                <i class="fas fa-star"></i> Score: {score}/10
            </span>
        </div>
        <div class="detail-item" data-tooltip="Movie Genre">
            <i class="fas fa-tags"></i> <span class="genre">{genre}</span>
        </div>
        <div class="votes">
            <i class="fas fa-thumbs-up"></i> Votes: {votes}
        </div>
    </div>
    """

    # Creating info plates for shortest and longest movies
    shortest_info_plate = info_plate_template.format(
        movie_name=shortest['movie_name'],
        rating=shortest['rating'],
        duration=shortest['duration'],
        score=shortest['score'],
        genre=shortest['genre'],
        votes=shortest['votes']
    )

    longest_info_plate = info_plate_template.format(
        movie_name=longest['movie_name'],
        rating=longest['rating'],
        duration=longest['duration'],
        score=longest['score'],
        genre=longest['genre'],
        votes=longest['votes']
    )

    # Combine info plates into scroller
    scroller=info_plates()
    scroller += f"{shortest_info_plate}{longest_info_plate}"
    st.html(scroller)


# 5️⃣ Plot: Ratings by Genre (Heatmap)
@st.cache_data
def plot_ratings_by_genre():
    df = fetch_data(
        "SELECT g.genre_name, ml.ratings FROM movie_list ml JOIN genres g ON ml.genre_id = g.genre_id",
        columns=["genre_name", "ratings"]
    )
    
    # Calculate average ratings
    avg_ratings = df.groupby('genre_name').mean().reset_index().round(2)
    avg_ratings_pivot = avg_ratings.pivot(index="genre_name", columns="ratings", values="ratings")

    # Create a figure and axes
    fig, ax = plt.subplots(figsize=(10, 8))  # Increase figure size for clarity

    # Create heatmap with improvements
    sns.heatmap(
        avg_ratings_pivot,
        annot=True,
        fmt=".2f",
        cmap="YlGnBu",
        linewidths=0.5,  # Add gridlines for readability
        cbar_kws={"shrink": 0.8},  # Shrink color bar for a cleaner look
        ax=ax
    )

    # Improve axis labels
    ax.set_title("Average Ratings by Genre", fontsize=24, fontweight='bold')
    ax.set_xlabel("Ratings", fontsize=18)
    ax.set_ylabel("Genre", fontsize=18)

    # Rotate x-axis labels for clarity
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)  # Keep y-axis labels horizontal

    st.pyplot(fig)

    st.write("""### 🔍 **Insights from the Heatmap:**
1. 🎭 **Top Rated Genres:** Genres like **History, War, and Game-Show** have the **highest average ratings** above **7.0**, indicating they are well-received by audiences.  

2. 😱 **Lowest Rated Genre:** **Horror** stands out with the **lowest average rating** around **5.53**, suggesting it might not appeal to a broad audience.  

3. 🎨 **Balanced Ratings:** Most genres have ratings between **6.0 and 6.5**, showing a relatively **consistent audience satisfaction** across these categories.  """)
# 6️⃣ Plot: Correlation Analysis (Scatter Plot)
@st.cache_data
def plot_correlation_analysis():
    df = fetch_data("SELECT ratings, votings FROM movie_list", columns=["ratings", "votings"])
    fig, ax = plt.subplots()
    sns.scatterplot(data=df, x='votings', y='ratings', ax=ax)
    ax.set_title("Correlation between Ratings and Votes")
    st.pyplot(fig)


if 'movie_count' not in st.session_state:
    st.session_state.movie_count=''




# top rated movies by genre
@st.cache_data    
def display_movie_details(select):
    select_query = f"""
        SELECT 
            ml.movie_name, 
            ml.duration, 
            ml.ratings, 
            ml.votings, 
            ml.score,
            g.genre_name
        FROM movie_list ml
        JOIN genres g ON ml.genre_id = g.genre_id
        WHERE lower(g.genre_name) = lower('{select}') 
        ORDER BY ml.score DESC LIMIT 10
    """
    tiny_scroller = info_plates() 
    movies = fetched_data(select_query)  # use diffrent function to fetch data from DB
    if movies:
        for movie in movies:
            movie_name, duration, rating, votes, score, genre = movie
            tiny_scroller += f"""
            <div class="info-plate">
                <div class="movie-name">{movie_name}</div>
                <div class="details-row">
                    <span class="detail-item" data-tooltip="Movie Rating">
                        <i class="fas fa-film"></i> Rating: {rating}
                    </span>
                    <span class="detail-item" data-tooltip="Duration">
                        <i class="fas fa-clock"></i> {duration} min
                    </span>
                    <span class="detail-item" data-tooltip="MYMDb Score">
                        <i class="fas fa-star"></i> Score: {score}/10
                    </span>
                </div>
                <div class="detail-item" data-tooltip="Movie Genre">
                    <i class="fas fa-tags"></i> <span class="genre">{genre}</span>
                </div>
                <div class="votes">
                    <i class="fas fa-thumbs-up"></i> Votes: {votes}
                </div>
            </div>"""
        tiny_scroller += "</body>"
        st.html(tiny_scroller) 
    elif movies and select !="select":
        st.write("No movies found for your criteria.")


# movie count by genre bar_plot
def plot_movie_count_by_genre():
    plot_query = """
        SELECT COUNT(ml.movie_name) AS movie_count, g.genre_name  
        FROM movie_list ml 
        JOIN genres g ON ml.genre_id = g.genre_id
        GROUP BY g.genre_name 
        ORDER BY movie_count DESC
    """
    movie_count = fetched_data(plot_query) #use different function to get
    if movie_count:
        movie_count_df = pd.DataFrame(movie_count, columns=['movie_count', 'genre_name'])
        fig, ax = plt.subplots(figsize=(10, 5))
        bars = ax.bar(movie_count_df["genre_name"], movie_count_df["movie_count"], color="cyan")
        ax.bar_label(bars, fmt='%d', padding=3, fontsize=6, color="black")
        ax.set_xlabel("Genre")
        ax.set_ylabel("Movie Count")
        ax.set_title("Movie Count by Genre")
        ax.set_xticklabels(movie_count_df["genre_name"], rotation=90)
        st.pyplot(fig)

#duration by genre bar_plot
@st.cache_data
def plot_avg_duration_by_genre():
    duration_query = """
        SELECT g.genre_name, AVG(ml.duration) AS avg_time 
        FROM movie_list ml
        JOIN genres g ON ml.genre_id = g.genre_id
        GROUP BY g.genre_name 
        ORDER BY avg_time DESC
    """
    avg_duration = fetched_data(duration_query)
    if avg_duration:
        avg_duration_df = pd.DataFrame(avg_duration, columns=["genre_name", "duration"])
        fig, ax = plt.subplots(figsize=(10, 5))
        bars = ax.bar(avg_duration_df["genre_name"], avg_duration_df["duration"], color="green")
        ax.bar_label(bars, fmt='%d', padding=3, fontsize=6, color="black", fontweight="bold")
        ax.set_xlabel("Genre")
        ax.set_ylabel("Average Duration")
        ax.set_title("Average Duration by Genre")
        ax.set_xticklabels(avg_duration_df["genre_name"], rotation=90)
        st.pyplot(fig)

#votings by genre bar_plot
@st.cache_data
def plot_avg_votings_by_genre():
    votings_query = """
        SELECT g.genre_name, AVG(ml.votings) AS avg_votings 
        FROM movie_list ml
        JOIN genres g ON ml.genre_id = g.genre_id
        GROUP BY g.genre_name 
        ORDER BY avg_votings DESC
    """
    avg_votings = fetched_data(votings_query)
    if avg_votings:
        avg_votings_df = pd.DataFrame(avg_votings, columns=["genre_name", "votings"])
        fig, ax = plt.subplots(figsize=(10, 5))
        bars = ax.bar(avg_votings_df["genre_name"], avg_votings_df["votings"], color="navy")
        ax.bar_label(bars, fmt='%d', padding=3, fontsize=6, color="black", fontweight="bold")
        ax.set_xlabel("Genre")
        ax.set_ylabel("Average Votings")
        ax.set_title("Average Votings by Genre")
        ax.set_xticklabels(avg_votings_df["genre_name"], rotation=90)
        st.pyplot(fig)








# 📊 Sidebar selectbox for plot selection
options = [
    "🎬 All Movie Insights",
    "📊 Movie Count by Genre",
    "⏱️ Average Duration by Genre",
    "👍 Average Votings by Genre",
    "⭐ Ratings Distribution",
    "🔥 Most Popular Genre by Votings",
    "🎥 Short vs. Long Movies by Runtime",
    "🌟 Average Ratings by Genre",
    "🔗 Correlation Analysis"
]

genre_list= ["Select an option","Action", "Adventure", "Animation", "Biography", "Comedy", "Crime", 
    "Documentary", "Drama", "Family", "Fantasy", "Game-Show", "History", 
    "Horror", "Music", "Musical", "Mystery", "News", "Reality-TV", 
    "Romance", "Sci-Fi", "Sport", "Talk-Show", "Thriller", "War", "Western"]

select=st.sidebar.selectbox("Top rated movies by genre",options=genre_list,index=0)

plot_option = st.sidebar.selectbox(
    "Choose a Plot",options=options)

if select !="select":
    display_movie_details(select)

if plot_option==options[1]:
    plot_movie_count_by_genre()
elif plot_option==options[2]:
    plot_avg_duration_by_genre()

elif plot_option==options[3]:
    plot_avg_votings_by_genre()
elif plot_option==options[4]:
    plot_rating_distribution()

elif plot_option == options[5]:
    plot_popular_genres()
elif plot_option == options[6]:
    plot_duration_extremes()
elif plot_option == options[7]:
    plot_ratings_by_genre()
elif plot_option == options[8]:
    plot_correlation_analysis()


def close_db():
    if conn and conn.open:
        conn.close()

atexit.register(close_db)