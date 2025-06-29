

import pickle
import streamlit as st
import requests

# Fetch movie poster from TMDB API
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return "https://via.placeholder.com/500"

# Recommend movies based on similarity
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))

    return recommended_movie_names, recommended_movie_posters

# Streamlit Page Configuration
st.set_page_config(page_title="Movie Recommender System", layout="wide")

# Load the data
movies = pickle.load(open('artificats/movie_list.pkl', 'rb'))
similarity = pickle.load(open('artificats/similary.pkl', 'rb'))

# Page Header
st.title("🎬 Movie Recommender System Using Machine Learning")
st.markdown("---")

# Movie Selection Dropdown
movie_list = movies['title'].values
selected_movie = st.selectbox("🔍 Select a movie to get recommendations:", movie_list)

# Show Recommendations
if st.button("✨ Show Recommendations"):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    # Display the movies in a grid format
    st.markdown("### 🎯 Top 5 Recommended Movies")
    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.image(recommended_movie_posters[i], use_container_width=True)
            st.write(recommended_movie_names[i])

# Footer
st.markdown("---")
st.caption("💡 Developed by Laxman Khedkar")






















