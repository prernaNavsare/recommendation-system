import pickle
import streamlit as st
import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters

st.set_page_config(page_title="Movie Recommender", page_icon=":clapper:", layout="wide") # Optional: Set page configuration

# CSS for animations and styling
st.markdown("""
<style>
body {
    font-family: sans-serif;
    background-color: #f0f0f0; /* Light background */
    color: #333;
}
.header {
    text-align: center;
    color: #d9534f; /* Example color */
    animation: fadeIn 1s ease-in-out; /* Fade in animation */
}
@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

.movie-container { /* Container for each movie */
    display: flex;
    flex-direction: column; /* Title above image */
    align-items: center; /* Center horizontally */
    margin: 10px; /* Add some spacing */
    animation: slideIn 0.5s ease-in-out; /* Slide in animation */
}

@keyframes slideIn {
    from { transform: translateY(20px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
}

.movie-title {
    font-size: 16px;
    font-weight: bold;
    margin-bottom: 5px;
    text-align: center;
}
.movie-poster {
    width: 150px;
    height: 225px;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    transition: transform 0.2s ease; /* Hover effect */
    cursor: pointer; /* Indicate clickability */
}
.movie-poster:hover {
    transform: scale(1.05); /* Slightly enlarge on hover */
    box-shadow: 0 6px 12px rgba(0,0,0,0.15); /* More shadow on hover */
}

.stSelectbox {
    width: 50%;
    margin: 20px auto;
}
.stButton {
    display: inline;
    margin: 20px auto;
    # background-color: #d9534f;
    color: white;
}

/* Optional: Style the columns for spacing */
.st-bf { /* Targets the outer container of the columns */
    gap: 20px; /* Adjust spacing as needed */
}
</style>
""", unsafe_allow_html=True)


st.markdown("<h1 class='header'>Movie Recommender System Using Machine Learning</h1>", unsafe_allow_html=True) # Apply header class

movies = pickle.load(open('./artifacts/movie_list.pkl','rb'))
similarity = pickle.load(open('./artifacts/similarity.pkl','rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    num_recommendations = len(recommended_movie_names)
    cols = st.columns(num_recommendations)

    for i in range(num_recommendations):
        with cols[i]:
            st.markdown(f"<div class='movie-container'><div class='movie-title'>{recommended_movie_names[i]}</div><img src='{recommended_movie_posters[i]}' class='movie-poster'></div>", unsafe_allow_html=True)
            # Or use st.image if you prefer:
            #st.image(recommended_movie_posters[i], use_column_width=False, caption=recommended_movie_names[i], css_classes=["movie-poster"])

