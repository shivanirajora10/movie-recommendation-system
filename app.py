import streamlit as st
import pickle
import pandas as pd
import requests
import os
import urllib.request

# Function to fetch movie poster from OMDb API
def fetch_poster(movie_title):
    api_key = "74f9f173"  # Replace with your OMDb API key
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    if data['Response'] == 'True' and 'Poster' in data:
        return data['Poster']
    else:
        return "https://via.placeholder.com/300x450?text=No+Poster+Found"

# Function to recommend movies
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []
    for i in movies_list:
        movie_title = movies.iloc[i[0]].title
        # Fetch poster for the movie
        poster_url = fetch_poster(movie_title)
        recommended_movies.append(movie_title)
        recommended_posters.append(poster_url)
    return recommended_movies, recommended_posters

# Load movie data and similarity matrix
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# Check if similarity.pkl exists, otherwise download it
file_path = 'similarity.pkl'
if not os.path.exists(file_path):
    url = "https://drive.google.com/uc?id=1_XWfuxX8g4NtT0OpU0bieU7CDpHbWkp5&export=download"
    urllib.request.urlretrieve(url, file_path)

similarity = pickle.load(open(file_path, 'rb'))

# Streamlit UI
st.title('Movie Recommender System')

# Add unique key to the selectbox
selected_movie_name = st.selectbox('Select a movie', movies['title'].values, key="movie_selectbox")

if st.button('Recommend'):
    recommendations, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.image(posters[0])
        st.text(recommendations[0])

    with col2:
        st.image(posters[1])
        st.text(recommendations[1])

    with col3:
        st.image(posters[2])
        st.text(recommendations[2])

    with col4:
        st.image(posters[3])
        st.text(recommendations[3])

    with col5:
        st.image(posters[4])
        st.text(recommendations[4])

    # Create 5 columns for the recommendations
    #cols = st.columns(5)
    # for col, movie, poster in zip(cols, recommendations, posters):
    #     with col:
    #         st.image(poster, use_container_width=True)  # Display the poster
    #         st.write(movie)  # Display the movie title
