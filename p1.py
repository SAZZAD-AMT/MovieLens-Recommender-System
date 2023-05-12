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

def get_recommendations(movie_title, movie_similarity, mean_ratings, movies, genres):
    idx = mean_ratings[mean_ratings['title'] == movie_title].index[0]
    sim_scores = list(enumerate(movie_similarity[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_indices = [i[0] for i in sim_scores[1:21]]
    recommended_movies = mean_ratings.iloc[sim_indices][['title', 'rating', 'movieId']]
    recommended_movies = pd.merge(recommended_movies, movies[['movieId', 'genres']], on='movieId')
    recommended_movies = recommended_movies[recommended_movies['genres'].str.contains(genres)]
    return recommended_movies

def suggest_movies(event=None):
    search_query = movie_entry.get().lower()
    filtered_movies = [movie for movie in movie_titles if search_query in movie.lower()]
    movie_listbox.delete(0, tk.END)
    for movie in filtered_movies:
        movie_listbox.insert(tk.END, movie)
    recommend_movies() 

def select_movie(event):
    selected_movie = movie_listbox.get(tk.ACTIVE)
    movie_entry.delete(0, tk.END)
    movie_entry.insert(tk.END, selected_movie)
    suggest_movies()
    recommend_movies()
    

def recommend_movies():
    movie_title = movie_entry.get()
    genres = genre_combobox.get()
    recommended_movies = get_recommendations(movie_title, movie_similarity, mean_ratings, movies, genres)
    movie_table.delete(*movie_table.get_children())
    for i, (index, row) in enumerate(recommended_movies.iterrows(), start=1):
        imdb_id = links[links['movieId'] == row['movieId']]['imdbId'].iloc[0]
        genres = row['genres']
        movie_table.insert('', tk.END, values=(i, row['title'], f"{row['rating']:.2f}", genres, imdb_id))

def refresh_movies():
    recommend_movies()
    
def reset_movies():
    movie_entry.delete(0, tk.END)
    genre_combobox.set('')
    movie_table.delete(*movie_table.get_children())
    movie_listbox.delete(0, tk.END)
    
window = tk.Tk()

window.title('Movie Recommendation System')
window.geometry('600x600')

genre_label = ttk.Label(window, text='SELECT MOVIES:')
genre_label.pack(pady=10)

movie_entry = ttk.Entry(window, width=50)
movie_entry.pack()
movie_entry.bind("<KeyRelease>", suggest_movies)

movie_label = ttk.Label(window, text='Suggest Movies: ')
movie_label.pack(pady=10)

movie_listbox = tk.Listbox(window, width=50)
movie_listbox.pack()
movie_listbox.bind("<ButtonRelease-1>", select_movie)
movie_listbox.bind("<<ListboxSelect>>", select_movie,recommend_movies)

genre_combobox = ttk.Combobox(window, width=50)

refresh_button = ttk.Button(window, text="Refresh", command=refresh_movies)
refresh_button.pack(pady=10,anchor='e')

reset_button = ttk.Button(window, text="RESET", command=reset_movies)
reset_button.pack(pady=10,anchor='e')

movie_table = ttk.Label(window, text='Recommended Movies: ')
movie_table.pack(pady=10)
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

window.mainloop()

