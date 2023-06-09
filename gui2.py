import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import tkinter as tk
from tkinter import ttk

movies = pd.read_csv('movies.csv')
ratings = pd.read_csv('ratings.csv')

movie_ratings = pd.merge(movies, ratings, on='movieId')

mean_ratings = movie_ratings.groupby(['movieId', 'title'])['rating'].mean().reset_index()

ratings_pivot = movie_ratings.pivot_table(index='userId', columns='title', values='rating').fillna(0)

movie_similarity = cosine_similarity(ratings_pivot)


def get_recommendations(movie_title, movie_similarity, mean_ratings):
    idx = mean_ratings[mean_ratings['title'] == movie_title].index[0]
    sim_scores = list(enumerate(movie_similarity[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_indices = [i[0] for i in sim_scores[1:11]]
    return mean_ratings.iloc[sim_indices][['title', 'rating']]

def recommend_movies():
    movie_title = movie_entry.get()
    recommended_movies = get_recommendations(movie_title, movie_similarity, mean_ratings)
    movie_table.delete(*movie_table.get_children())
    for i, (index, row) in enumerate(recommended_movies.iterrows(), start=1):
        movie_table.insert('', tk.END, values=(i, row['title'], f"{row['rating']:.2f}"))

window = tk.Tk()
window.title('Movie Recommendation System')
window.geometry('600x400')

movie_label = ttk.Label(window, text='Enter a movie title:')
movie_label.pack(pady=10)
movie_entry = ttk.Entry(window,width=50)
movie_entry.pack()

recommend_button = ttk.Button(window, text='Recommend Movies', command=recommend_movies)
recommend_button.pack(pady=10)

movie_table = ttk.Treeview(window, columns=('SL','Movie', 'Rating'), show='headings', height=10)
movie_table.heading('SL', text='SL')
movie_table.heading('Movie', text='Movie')
movie_table.heading('Rating', text='Rating')
movie_table.pack(pady=10)
movie_table.column('SL', width=10, anchor='center')
movie_table.column('Movie', width=400, anchor='center')
movie_table.column('Rating', width=80, anchor='center')

def clear_movies():
    movie_entry.delete(0, tk.END)
    movie_table.delete(*movie_table.get_children())

clear_button = ttk.Button(window, text='RESET', command=clear_movies)
clear_button.pack(pady=10)

window.mainloop()