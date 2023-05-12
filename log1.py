
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

username_label = ttk.Label(login_window, text='Username:')
username_label.pack(pady=10)

username_entry = ttk.Entry(login_window)
username_entry.pack()

password_label = ttk.Label(login_window, text='Password:')
password_label.pack(pady=10)

password_entry = ttk.Entry(login_window, show='*')
password_entry.pack()

def save_user_data(username, password):
    with open('users.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, password])

# Function to check if the username and password match
def check_credentials(username, password):
    with open('users.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == username and row[1] == password:
                return True
    return False

# Function to handle the login process
def login():
    username = username_entry.get()
    password = password_entry.get()

    if check_credentials(username, password):
        login_window.destroy()
        open_movie_recommendation_system()
    else:
        error_label.config(text='Invalid username or password')

# Function to handle the signup process
def signup():
    username = username_entry.get()
    password = password_entry.get()

    if username and password:
        save_user_data(username, password)
        error_label.config(text='Signup successful. Please login.')
    else:
        error_label.config(text='Username and password are required.')


error_label = ttk.Label(login_window, text='', foreground='red')
error_label.pack()

login_button = ttk.Button(login_window, text='Login', command=login)
login_button.pack(pady=10)
      
signup_button = ttk.Button(login_window, text='Signup', command=signup)
signup_button.pack(pady=10)

def open_movie_recommendation_system():
    import p1
    
# Start the login window
login_window.mainloop()
