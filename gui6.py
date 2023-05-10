import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import tkinter as tk
from tkinter import ttk

movies = pd.read_csv('movies.csv')
ratings = pd.read_csv('ratings.csv')
links = pd.read_csv('links.csv')
tags = pd.read_csv('tags.csv')

movie_ratings = pd.merge(movies, ratings, on='movieId')
mean_ratings = movie_ratings.groupby(['movieId', 'title'])['rating'].mean().reset_index()
ratings_pivot = movie_ratings.pivot_table(index='userId', columns='title', values='rating').fillna(0)
print(ratings_pivot)
movie_similarity = cosine_similarity(ratings_pivot)

movie_titles = list(movies['title'])

def get_recommendations(movie_title, movie_similarity, mean_ratings, movies):
    idx = mean_ratings[mean_ratings['title'] == movie_title].index[0]
    sim_scores = list(enumerate(movie_similarity[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_indices = [i[0] for i in sim_scores[1:21]]
    recommended_movies = mean_ratings.iloc[sim_indices][['title', 'rating', 'movieId']]
    recommended_movies = pd.merge(recommended_movies, movies[['movieId', 'genres']], on='movieId')
    return recommended_movies

def recommend_movies():
    movie_title = movie_combobox.get()
    recommended_movies = get_recommendations(movie_title, movie_similarity, mean_ratings, movies)
    movie_table.delete(*movie_table.get_children())
    for i, (index, row) in enumerate(recommended_movies.iterrows(), start=1):
        imdb_id = links[links['movieId'] == row['movieId']]['imdbId'].iloc[0]
        genres = row['genres']
        movie_table.insert('', tk.END, values=(i, row['title'], f"{row['rating']:.2f}", genres, imdb_id))



window = tk.Tk()
window.title('Movie Recommendation System')
window.geometry('600x600')

movie_label = ttk.Label(window, text='Select a movie:')
movie_label.pack(pady=10)
def update_movie_list(event=None):
    search_query = movie_combobox.get()
    if search_query:
        filtered_movies = [movie for movie in movie_titles if search_query.lower() in movie.lower()]
    else:
        filtered_movies = movie_titles
    movie_combobox.config(values=filtered_movies)

movie_combobox = ttk.Combobox(window, width=50)
movie_combobox.pack()

movie_combobox.bind("<KeyRelease>", update_movie_list)


recommend_button = ttk.Button(window, text='Recommend Movies', command=recommend_movies)
recommend_button.pack(pady=10)

movie_table = ttk.Treeview(window, columns=('SL', 'Movie', 'Rating', 'Genres'), show='headings', height=20)
movie_table.heading('SL', text='SL')
movie_table.heading('Movie', text='Movie')
movie_table.heading('Rating', text='Rating')
movie_table.heading('Genres', text='Genres')
movie_table.pack(pady=10)
movie_table.column('SL', width=10, anchor='center')
movie_table.column('Movie', width=300, anchor='center')
movie_table.column('Rating', width=80, anchor='center')
movie_table.column('Genres', width=200, anchor='center')


def clear_movies():
    movie_combobox.set('')
    movie_table.delete(*movie_table.get_children())

clear_button = ttk.Button(window, text='RESET', command=clear_movies)
clear_button.pack(pady=10)
#
window.mainloop()
