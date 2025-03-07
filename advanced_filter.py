import streamlit as st
import pymysql
import atexit
from tenacity import retry, stop_after_attempt, wait_fixed
import connect
from scroller import info_plates
info_plates=info_plates()


conn = connect.connect_db()  #connect db using connect_db from connect





   
# Initialize session state variables
if 'movies' not in st.session_state:
    st.session_state.movies = []
# we add session state for load lazy scroll
if 'lazy_scroll' not in st.session_state:
    st.session_state.lazy_scroll = 10
if 'filters' not in st.session_state:
    st.session_state.filters = {}



# Sidebar Filters Section
st.sidebar.markdown('<p class="sidebar-heading">Advanced Search options</p>', unsafe_allow_html=True)

# Genres Filter
with st.sidebar.expander("🎬 Select Genre(s)", expanded=False):
    genres = st.multiselect("Select genres:", ["Action", "Adventure", "Animation", "Biography", "Comedy", "Crime", 
    "Documentary", "Drama", "Family", "Fantasy", "Game-Show", "History", 
    "Horror", "Music", "Musical", "Mystery", "News", "Reality-TV", 
    "Romance", "Sci-Fi", "Sport", "Talk-Show", "Thriller", "War", "Western"])

# Ratings Filter
with st.sidebar.expander("⭐ Select Ratings Range", expanded=False):
    ratings = st.slider("Ratings", min_value=0.0, max_value=10.0, value=(0.0, 10.0), step=0.1, format="%.1f")

# Votes Filter
with st.sidebar.expander("🗳️ Votes Range", expanded=False):
    votes_from = st.number_input("From", min_value=6, max_value=151000, step=100, value=6, format="%d")
    votes_to = st.number_input("To", min_value=6, max_value=151000, step=100, value=151000, format="%d")

# Duration Filter
with st.sidebar.expander("⏳ Select Duration Range", expanded=False):
    duration_range = st.slider("Duration", min_value=30, max_value=300, value=(30, 300), step=5, format="%d min")

# Score Filter
with st.sidebar.expander("🏆 Select MYMDb Score Range", expanded=False,):
    score_range = st.slider("Score", min_value=0.0, max_value=10.0, value=(0.0, 10.0), step=0.1, format="%.1f",help="The MYMDB Score balances ratings and vote counts to rank movies fairly. It prevents movies with few votes but high ratings from dominating and gives more weight to movies with many positive votes." )

# Submit Button
submit = st.sidebar.button("🌐 Submit Filters")

#search box
with st.form("search_form")  :
    col1, col2 = st.columns([0.85, 0.15], vertical_alignment="center",gap="medium")
    with col1:  
        search_query = st.text_input("🔍 Search for a Movie", placeholder="Type a movie name...")
    with col2:
        search_submitted = st.form_submit_button("Search")


#fetching data from the db
@st.cache_data
def fetch_movies_from_db():
    """Fetch movies from database using current filters"""
    if st.session_state.filters.get('search_query'): #search box 
        # SEARCH-SPECIFIC QUERY (ONLY NAME SEARCH)
        base_query = """
            SELECT 
                ml.movie_name, 
                ml.duration, 
                ml.ratings, 
                ml.votings, 
                ml.score,
                GROUP_CONCAT(
                    DISTINCT g.genre_name
                    ORDER BY g.genre_name SEPARATOR ', '
                ) AS genre_names
            FROM movie_list ml
            JOIN genres g ON ml.genre_id = g.genre_id
            WHERE LOWER(ml.movie_name) LIKE LOWER(%s)
            GROUP BY 
                ml.movie_name, 
                ml.duration, 
                ml.ratings, 
                ml.votings, 
                ml.score
            ORDER BY ml.score DESC
        """
        search_term = f"%{st.session_state.filters['search_query']}%"
        params = [search_term]
        
    else:
        # FILTER-SPECIFIC QUERY
        base_query = """
            SELECT 
                ml.movie_name, 
                ml.duration, 
                ml.ratings, 
                ml.votings, 
                ml.score,
                GROUP_CONCAT(
                    DISTINCT g.genre_name
                    ORDER BY g.genre_name SEPARATOR ', '
                ) AS genre_names
            FROM movie_list ml
            JOIN genres g ON ml.genre_id = g.genre_id
        """
        
        conditions = []
        params = []
        
        # Build filter conditions

        #genres filter condition
        if st.session_state.filters.get('genres'):
            placeholders = ', '.join(['%s'] * len(st.session_state.filters['genres']))
            conditions.append(f"g.genre_name IN ({placeholders})")
            params.extend(st.session_state.filters['genres'])
        #ratings filter condition
        if st.session_state.filters.get('ratings') != (0.0, 10.0):
            conditions.append("ml.ratings BETWEEN %s AND %s")
            params.extend(st.session_state.filters['ratings'])
        #votings filter condition
        if st.session_state.filters.get('votes') != (6, 151000):
            conditions.append("ml.votings BETWEEN %s AND %s")
            params.extend(st.session_state.filters['votes'])
        #duration filetr condtion
        if st.session_state.filters.get('duration') != (30, 300):
            conditions.append("ml.duration BETWEEN %s AND %s")
            params.extend(st.session_state.filters['duration'])
        #mymdb score filter condition
        if st.session_state.filters.get('score') != (0.0, 10.0):
            conditions.append("ml.score BETWEEN %s AND %s")
            params.extend(st.session_state.filters['score'])

        # Add WHERE clause if needed
        if conditions:
            base_query += " WHERE " + " AND ".join(conditions)

        # Add GROUP BY and HAVING
        base_query += """
            GROUP BY 
                ml.movie_name, 
                ml.duration, 
                ml.ratings, 
                ml.votings, 
                ml.score
        """
        # add having only for genres filter option
        if st.session_state.filters.get('genres'):
            base_query += f" HAVING COUNT(DISTINCT g.genre_name) = {len(st.session_state.filters['genres'])}"
        
        base_query += " ORDER BY ml.score DESC"


    #fetch the data from DB
    with conn.cursor() as cursor:
        cursor.execute(base_query, tuple(params))
        return cursor.fetchall()
#session-state for search box
if search_submitted and search_query:
    st.session_state.filters = {
        'search_query': search_query.strip().lower(),
        'genres': [],
        'ratings': (0.0, 10.0),
        'votes': (6, 151000),
        'duration': (30, 300),
        'score': (0.0, 10.0)
        
    }
    st.session_state.movies = fetch_movies_from_db()
    st.session_state.lazy_scroll = 10


#session state condition for advanced filter
if submit:
    # Store current filters in session state
    st.session_state.filters = {
        'genres': genres,
        'ratings': ratings,
        'votes': (votes_from, votes_to),
        'duration': duration_range,
        'score': score_range,
        'search_query': ''
    
    }
    
    # Fetch movies and reset scroll
    st.session_state.movies = fetch_movies_from_db()
    st.session_state.lazy_scroll = 10



    
# Display movies from session state
if st.session_state.movies:
    scroller = info_plates # the html content is info plates
    for movie in st.session_state.movies[:st.session_state.lazy_scroll]:
        movie_name, duration, rating, votes, score, genre = movie
        scroller += f"""
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
    
    scroller += "</body>"
    st.html(scroller)  # show the infoplates

    
    # Load More button
    if st.session_state.lazy_scroll < len(st.session_state.movies):
        if st.button("Load More"):
            st.session_state.lazy_scroll += 10
            st.rerun()


elif submit:  # Handle case when no results found while advanced filter
    st.warning("No movies found matching your criteria.")

elif search_query: # handle case when no results in search box
    st.warning("No movies found please check the spelling of the movie")

# Closing Database Connection Properly
  
def close_db():
    if conn and conn.open:
        conn.close()

atexit.register(close_db)



