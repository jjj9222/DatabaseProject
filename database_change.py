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

def getSongQuery():
    # Deletes the info in the listbox on press of button
    song_listbox.delete(0, END)

    if (song_var.get() == ""):
        pass
    elif (song_var.get() == "*"):
        cursor.execute("""SELECT title from song""")
        data = cursor.fetchall()
        for row in data:
            song_listbox.insert(END, row[0])
    else:
        try:
            query = "SELECT title from song where title like '%" + song_var.get() + "%'"
            cursor.execute(query)
            data = cursor.fetchall()
            for row in data:
                song_listbox.insert(END, row[0])
        except:
            print("Invalid Query")

def getArtistQuery():
    # Deletes the info in the listbox on press of button
    artist_listbox.delete(0, END)

    if (artist_var.get() == ""):
        pass
    elif (artist_var.get() == "*"):
        cursor.execute("""SELECT "firstName", "lastName" from artist""")
        data = cursor.fetchall()
        for row in data:
            artist_listbox.insert(END, row)
    else:
        try:
            query = "SELECT \"firstName\", \"lastName\" from artist where \"firstName\" like '%" + artist_var.get() + "%' or \"lastName\" like '%" + artist_var.get() + "%'"
            cursor.execute(query)
            data = cursor.fetchall()
            for row in data:
                artist_listbox.insert(END, row)
        except:
            print("Invalid Query")

def getAlbumQuery():
    # Deletes the info in the listbox on press of button
    album_listbox.delete(0, END)

    if (album_var.get() == ""):
        pass
    elif (album_var.get() == "*"):
        cursor.execute("""SELECT "albumName" from album""")
        data = cursor.fetchall()
        for row in data:
            album_listbox.insert(END, row)
    else:
        try:
            query = "SELECT \"albumName\" from album where \"albumName\" like '%" + album_var.get() + "%'"
            print(query)
            cursor.execute(query)
            data = cursor.fetchall()
            for row in data:
                album_listbox.insert(END, row)
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
artist_scoll.grid(row=1, column=30, rowspan=10, sticky=N+S+W)
artist_listbox = Listbox(width=50, yscrollcommand=artist_scoll.set)
artist_listbox.grid(row=1, column=20)
artist_scoll.config(command=artist_listbox.yview)

album_label = Label(window, text="Album Name")
album_label.grid(column=40, row=0)
album_scoll = Scrollbar(window)
album_scoll.grid(row=1, column=50, rowspan=10, sticky=N+S+W)
album_listbox = Listbox(width=50, yscrollcommand=album_scoll.set)
album_listbox.grid(row=1, column=40)
album_scoll.config(command=album_listbox.yview)

song_var = StringVar()
artist_var = StringVar()
album_var = StringVar()

song_entry = Entry(window, textvariable=song_var)
song_entry.grid(row=10)

artist_entry = Entry(window, textvariable=artist_var)
artist_entry.grid(row=10, column=20)

album_entry = Entry(window, textvariable=album_var)
album_entry.grid(row=10, column=40)

song_button = Button(window, text="Search", command=getSongQuery)
song_button.grid(row=15)

artist_button = Button(window, text="Search", command=getArtistQuery)
artist_button.grid(row=15, column=20)

album_button = Button(window, text="Search", command=getAlbumQuery)
album_button.grid(row=15, column=40)

window.mainloop()

