import tkinter as tk
from tkinter import ttk

# Create a custom style
style = ttk.Style()
style.configure("TLabel", 
                background="lightblue", 
                foreground="black", 
                font=("Helvetica", 16), 
                padding=10)
style.configure("TButton", 
                background="lightgreen", 
                foreground="black", 
                font=("Helvetica", 16), 
                padding=10)
style.configure("TEntry", 
                background="white", 
                foreground="black", 
                font=("Helvetica", 16))
style.configure("TListbox",
                background="white",
                foreground="black",
                font=("Helvetica", 12))
style.configure("Treeview",
                background="white",
                foreground="black",
                font=("Helvetica", 12))

# Create the main window
window = tk.Tk()
window.title("My Application")
window.geometry("800x600")
window.configure(background="lightblue")

# Create a logo label
logo_label = ttk.Label(window, text="My Logo")
logo_label.grid(row=0, column=0, padx=10, pady=10)

# Create a user ID label
user_id_label = ttk.Label(window, text="User ID")
user_id_label.grid(row=1, column=0, padx=10, pady=10)

# Create a user ID entry
user_id_entry = ttk.Entry(window)
user_id_entry.grid(row=1, column=1, padx=10, pady=10)

# Create a login button
login_button = ttk.Button(window, text="Login")
login_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# Create a listbox for movie suggestions
movie_listbox = tk.Listbox(window, width=50)
movie_listbox.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Create a treeview for recommended movies
movie_treeview = ttk.Treeview(window, columns=('Movie', 'Rating', 'Genres'), show='headings', height=20)
movie_treeview.heading('Movie', text='Movie')
movie_treeview.heading('Rating', text='Rating')
movie_treeview.heading('Genres', text='Genres')
movie_treeview.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

window.mainloop()
