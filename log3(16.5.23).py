
import tkinter as tk
from tkinter import ttk
import csv


login_window = tk.Tk()
login_window.title('Login')
login_window.geometry('500x400')

logo_image = tk.PhotoImage(file='logo.png')
logo_image = logo_image.subsample(4, 4)
logo_label = ttk.Label(login_window, image=logo_image)
logo_label.pack(pady=10)

user_id_label = ttk.Label(login_window, text='User ID:')
user_id_label.pack(pady=10)

user_id_entry = ttk.Entry(login_window)
user_id_entry.pack()


def check_user_id(user_id):
    with open('ratings.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            if row[0] == user_id:
                return True
    return False

def login(event=None):
    user_id = user_id_entry.get()
    
    if check_user_id(user_id):
        login_window.destroy()
        open_movie_recommendation_system(user_id)
    else:
        error_label.config(text='Invalid user ID')

error_label = ttk.Label(login_window, text='', foreground='red')
error_label.pack()

login_window.bind('<Return>', login)
login_button = ttk.Button(login_window, text='Login', command=login)
login_button.pack(pady=10)


def open_movie_recommendation_system(user_id):
   
    import pandas as pd
    import numpy as np
    from sklearn.metrics.pairwise import cosine_similarity
    import time

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
        
        if movie_title not in mean_ratings['title'].values:
            print(f"Movie '{movie_title}' not found in the database.")
            return pd.DataFrame()  # Return an empty DataFrame

        idx = mean_ratings[mean_ratings['title'] == movie_title].index[0]
        print(idx)
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
        recommend_movies()        

    def recommend_movies():
        
        movie_title = movie_entry.get()
        genres = genre_combobox.get()
        recommended_movies = get_recommendations(movie_title, movie_similarity, mean_ratings, movies, genres)
        movie_table.delete(*movie_table.get_children())
        
        for i, (index, row) in enumerate(recommended_movies.iterrows(), start=1):
            imdb_id = links[links['movieId'] == row['movieId']]['imdbId'].iloc[0]
            genres = row['genres']
            movie_table.insert('', tk.END, values=(row['title'], f"{row['rating']:.2f}", genres, imdb_id))
      
    def refresh_movies():
        recommend_movies()
            
    def rate_movie():
        selected_movie = movie_table.selection()
        if not selected_movie: 
            return
        movie_info = movie_table.item(selected_movie)
        movie_title = movie_info['values'][0]
        
        selected_movie = movie_table.focus()
        movie_info = movie_table.item(selected_movie)
        movie_title = movie_info['values'][0]
        
        rating_window = tk.Toplevel(window)
        rating_window.title("Rate Movie")
        rating_window.geometry('300x125')
        
        rating_label = ttk.Label(rating_window, text=f"Rate '{movie_title}':")
        rating_label.pack(pady=10)
        
        rating_entry = ttk.Entry(rating_window, width=10)
        rating_entry.pack(pady=10)
        
        submit_button = ttk.Button(rating_window, text="Submit", command=lambda: save_rating(movie_title, rating_entry.get()))
        submit_button.pack(pady=10)
        
        rating_window.mainloop()     
        
    import csv
    from tkinter import messagebox
    
    def save_rating(movie_title, rating):
        try:
            rating = float(rating)
            if rating < 1 or rating > 5:
                raise ValueError()

            movie_id = mean_ratings[mean_ratings['title'] == movie_title]['movieId'].iloc[0]

            with open('user_ratings.csv', 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['User_ID'] == str(user_id) and row['Movie'] == movie_title:
                        messagebox.showerror("Error", "You have already rated this movie.")
                        return

            new_rating = {'User_ID': user_id, 'Movie': movie_title, 'Rating': rating}

            with open('user_ratings.csv', 'a', newline='') as file:
                fieldnames = ['User_ID', 'Movie', 'Rating']
                writer = csv.DictWriter(file, fieldnames=fieldnames)

                if file.tell() == 0:
                    writer.writeheader()

                writer.writerow(new_rating)
                
            ratings = ratings.append(new_rating, ignore_index=True)
            ratings_pivot = movie_ratings.pivot_table(index='userId', columns='title', values='rating').fillna(0)
            movie_similarity = cosine_similarity(ratings_pivot)
            recommend_movies()

            messagebox.showinfo("Success", "Rating saved successfully!")
        except (ValueError, IndexError):
            messagebox.showerror("Error", "Invalid rating or movie not found!")
             
    window = tk.Tk()

    window.title(f'Movie Recommendation System-------User ID: {user_id}')
    window.geometry('600x600')

    genre_label = ttk.Label(window, text='SELECT MOVIES:')
    genre_label.pack(pady=10)

    movie_entry = ttk.Entry(window, width=50)
    movie_entry.pack()
    movie_entry.bind("<KeyRelease>", suggest_movies)
    movie_entry.bind('<Return>', recommend_movies)

    movie_label = ttk.Label(window, text='Suggest Movies: ')
    movie_label.pack(pady=10)

    movie_listbox = tk.Listbox(window, width=50)
    movie_listbox.pack()
    movie_listbox.bind("<ButtonRelease-1>", select_movie)
    movie_listbox.bind("<<ListboxSelect>>", select_movie,recommend_movies)
    genre_combobox = ttk.Combobox(window, width=50)
    movie_listbox.bind('<<ListboxSelect>>', select_movie)

    refresh_button = ttk.Button(window, text="Refresh", command=refresh_movies)
    refresh_button.pack(pady=10,anchor='e')

    movie_table = ttk.Label(window, text='Recommended Movies: ')
    movie_table.pack(pady=10)
    movie_table = ttk.Treeview(window, columns=('Movie', 'Rating', 'Genres'), show='headings', height=20)
    
    movie_table.bind("<Double-1>", lambda e: rate_movie())

    movie_table.heading('Movie', text='Movie')
    movie_table.heading('Rating', text='Rating')
    movie_table.heading('Genres', text='Genres')
    movie_table.pack(pady=10)

    movie_table.column('Movie', width=300, anchor='center')
    movie_table.column('Rating', width=80, anchor='center')
    movie_table.column('Genres', width=200, anchor='center')
    
    window.mainloop()


login_window.mainloop()
