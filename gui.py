import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import tkinter as tk
from tkinter import ttk

# Load the datasets
movies = pd.read_csv('movies.csv')
ratings = pd.read_csv('ratings.csv')

# Merge the movies and ratings dataframes
movie_ratings = pd.merge(movies, ratings, on='movieId')

# Calculate the mean rating for each movie
mean_ratings = movie_ratings.groupby(['movieId', 'title'])['rating'].mean().reset_index()

# Pivot the ratings dataframe to create a matrix of user ratings
ratings_pivot = movie_ratings.pivot_table(index='userId', columns='title', values='rating').fillna(0)

# Calculate the similarity between movies based on their ratings
movie_similarity = cosine_similarity(ratings_pivot)

# Create a function to recommend movies based on the input movie
def get_recommendations(movie_title, movie_similarity, mean_ratings):
    # Get the index of the input movie
    idx = mean_ratings[mean_ratings['title'] == movie_title].index[0]
    # Get the similarity scores for all movies
    sim_scores = list(enumerate(movie_similarity[idx]))
    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    # Get the indices of the top 10 similar movies
    sim_indices = [i[0] for i in sim_scores[1:11]]
    # Return the titles and average ratings of the top 10 similar movies
    return mean_ratings.iloc[sim_indices][['title', 'rating']]

# Create a GUI for the user to input a movie title
def recommend_movies():
    # Get the user input from the text box
    movie_title = movie_entry.get()
    # Call the get_recommendations function to recommend movies based on the input movie
    recommended_movies = get_recommendations(movie_title, movie_similarity, mean_ratings)
    # Display the recommended movies and their ratings in the list box
    movie_list.delete(0, tk.END)
   
    for index, row in recommended_movies.iterrows():
        movie_list.insert(tk.END, f"{row['title']} ---------------- {row['rating']:.2f}")

# Create a window for the GUI
window = tk.Tk()
window.title('Movie Recommendation System')
window.geometry('400x400')

# Create a label and text box for the user to input a movie title
movie_label = ttk.Label(window, text='Enter a movie title:')
movie_label.pack(pady=10)
movie_entry = ttk.Entry(window,width=50)
movie_entry.pack()

# Create a button to recommend movies based on the user's input
recommend_button = ttk.Button(window, text='Recommend Movies', command=recommend_movies)
recommend_button.pack(pady=10)

heading_label = ttk.Label(window, text='Movie                                Rating')
heading_label.pack()
# Create a list box to display the recommended movies and their ratings
movie_list = tk.Listbox(window,width=60)
movie_list.pack(pady=10)

# Create a function to clear the input text box and the list box
def clear_movies():
    movie_entry.delete(0, tk.END)
    movie_list.delete(0, tk.END)

# Create a button to clear the input text box and the list box
clear_button = ttk.Button(window, text='RESET', command=clear_movies)
clear_button.pack(pady=10)

# Start the GUI
window.mainloop()
