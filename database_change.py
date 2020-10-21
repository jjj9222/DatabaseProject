import psycopg2
from tkinter import *

hostname = 'reddwarf.cs.rit.edu'
username = 'p320_02'
password = 'Eux5iothoo3WaeL7yahM'
database = 'p320_02'

# create connection to db
connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)

# Cursor for the database
cursor = connection.cursor()

def getQuery():
    print(song_var.get())
    if (song_var == ""):
        pass
    elif (song_var == "*"):
        print("in")
        cursor.execute("""SELECT title from song""")
        data = cursor.fetchall()
        for row in data:
            song_listbox.insert(END, row[0])
    else:
        try:
            query = "SELECT title from song where title like %" + song_var + "%"
            cursor.execute(query)
            data = cursor.fetchall()
            for row in data:
                song_listbox.insert(END, row[0])
        except:
            print("Invalid Query")


window = Tk()
window.title("Music Player")
window.geometry("1000x500")

#Getting Song Browser Setup
song_label = Label(window, text="Song Name")
song_label.grid(column=0)
song_scoll = Scrollbar(window)
song_scoll.grid(row=1, column=1, rowspan=10, sticky=N+S+W)
song_listbox = Listbox(width=50, yscrollcommand=song_scoll.set)
song_listbox.grid(row=1)
song_scoll.config(command=song_listbox.yview)

artist_label = Label(window, text="Artist Name")
artist_label.grid(column=20, row=0)
artist_scoll = Scrollbar(window)
artist_scoll.grid(row=1, column=20, rowspan=10)
artist_listbox = Listbox(width=50, yscrollcommand=artist_scoll.set)
artist_listbox.grid(row=1, column=20)
artist_scoll.config(command=artist_listbox.yview)

album_label = Label(window, text="Album Name")
album_label.grid(column=42, row=0)
album_scoll = Scrollbar(window)
album_scoll.grid(row=1, column=42, rowspan=10)
album_listbox = Listbox(width=50, yscrollcommand=album_scoll.set)
album_listbox.grid(row=1, column=42)
album_scoll.config(command=album_listbox.yview)

song_var = StringVar()

song_entry = Entry(window, textvariable=song_var)
song_entry.grid(row=10)

but = Button(window, text="Search", command=getQuery)
but.grid(row=15)

window.mainloop()

