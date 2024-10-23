import streamlit as st
import numpy as np
import pandas as pd
import pickle

movie_details = pickle.load(open('./movie_details.pkl', 'rb'))

st.title('Ree Recommender 2.0')

option = st.selectbox(
    "Choose a Movie",
    sorted(movie_details['title'].values),
)

selected_movie = option


def load_chunk(movie_index, chunk_size=300):
    chunk_no = movie_index // chunk_size
    chunk = pickle.load(open(f'./similarity_matrix/chunk{chunk_no}.pkl', 'rb'))
    return chunk


def return_similarity_vector(movie_index, similarity_matrix_chunk, chunk_size=300):
    similarity_vector_index = movie_index % chunk_size
    similarity_vector = similarity_matrix_chunk[similarity_vector_index]
    return similarity_vector


def recommend(movie):
    movie_index = movie_details.loc[movie_details['title'] == movie].index[0]

    similarity_matrix_chunk = load_chunk(movie_index)
    similarity_vector = return_similarity_vector(movie_index, similarity_matrix_chunk)

    top_5 = sorted(list(enumerate(similarity_vector)), key=(lambda x : x[1]), reverse=True)
    top_5 = top_5[1:6]
    top_5_index = [i[0] for i in top_5]
    top_5_movies = movie_details.loc[top_5_index, 'title'].values
    top_5_movies_id = movie_details.loc[top_5_index, 'movie_id'].values
    # del similarity_matrix_chunk    # to free up memory used by the chunk

    return top_5_movies_id, top_5_movies

def fetch_poster(movie_id):
    poster_path = movie_details.loc[movie_details['movie_id'] == movie_id, 'poster_path'].values[0]
    poster_url = f'https://image.tmdb.org/t/p/w185/{poster_path}'
    return poster_url

if st.button("Recommend"):
    recommended_movie_id, recommended_movie_names = recommend(selected_movie)

    columns = [col1, col2, col3, col4, col5] = st.columns(5)
    for col_no in range(len(columns)):
        with columns[col_no]:
            movie_id, movie_name = recommended_movie_id[col_no], recommended_movie_names[col_no]
            poster_url = fetch_poster(movie_id)
            st.image(poster_url, caption=movie_name)




