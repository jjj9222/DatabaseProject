import psycopg2
import tkinter as tk
from tkinter import simpledialog


if __name__ == '__main__':
    # Connection to the database
    connection = psycopg2.connect(host="reddwarf.cs.rit.edu", database="p320_02", user="p320_02", password="Eux5iothoo3WaeL7yahM")

    # Cursor for the database
    cursor = connection.cursor()

    cursor.execute("""SELECT title from song""")

    data = cursor.fetchall()

    window = tk.Tk()
    window.title("Music Collection Interface")
    window.rowconfigure(0, minsize=3000, weight=1)
    window.columnconfigure(0, minsize=3000, weight=1)
    window.geometry("1000x500")
    song_label = tk.Label(text="Song Name")
    entry = tk.Entry()
    # Making the list that displays the songs
    song_listbox = tk.Listbox(width=50)
    album_listbox = tk.Listbox()

    song_label.pack()
    song_listbox.pack()



    song_listbox.insert(0, "a list entry")
    for row in data:
        song_listbox.insert(tk.END, row[0])

    window.mainloop()

