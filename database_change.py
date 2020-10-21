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
    #list = song_listbox.get(song_listbox.curselection())
    #print(list)

    if (song_var.get() == ""):
        pass
    elif (song_var.get() == "*"):
        cursor.execute("""SELECT title from song""")
        data = cursor.fetchall()
        for row in data:
            song_listbox.insert(END, row[0])

        #display all artists that sing songs, all albums that have songs in them
        query = "SELECT A.\"firstName\", A.\"lastName\" from artist A, song S, performed P where P.\"artistID\" = A.\"artistID\" AND P.id = S.id"
        cursor.execute(query)
        data = cursor.fetchall()
        artist_listbox.delete(0, END)
        for row in data:
            artist_listbox.insert(END, row)

    else:
        try:
            query = "SELECT title from song where title like '%" + song_var.get() + "%'"
            cursor.execute(query)
            data = cursor.fetchall()
            for row in data:
                song_listbox.insert(END, row[0])
        except:
            print("Invalid Query")

        try:
            query = "SELECT id from song where title like '%" + song_var.get() + "%'"
            cursor.execute(query)
            data = cursor.fetchall()
            artist_listbox.delete(0, END)
            for number in data:
                query = "SELECT DISTINCT A.\"firstName\", A.\"lastName\" from artist A, song S, performed P where P.\"artistID\" = A.\"artistID\" AND P.id = {0[0]}".format(number)
                cursor.execute(query)
                data = cursor.fetchall()
                for row in data:
                    artist_listbox.insert(END, row)
        except:
            print("Error")


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

def curSongSelect(event):
    widget = event.widget
    cursor_select = widget.curselection()
    try:
        song_var.set(widget.get(cursor_select[0]))
    except:
        pass
    print(song_var)

def curArtistSelect(event):
    widget = event.widget
    cursor_select = widget.curselection()
    try:
        artist_var.set(widget.get(cursor_select[0]))
    except:
        pass

def curAlbumSelect(event):
    widget = event.widget
    cursor_select = widget.curselection()
    try:
        album_var.set(widget.get(cursor_select[0]))
    except:
        pass


def createEntry():
    return 1


window = Tk()
window.title("Music Player")
window.geometry("1000x750")

#Getting Song Browser Setup
song_label = Label(window, text="Song Name")
song_label.grid(column=0)
song_scoll = Scrollbar(window)
song_scoll.grid(row=1, column=1, rowspan=10, sticky=N+S+W)
song_listbox = Listbox(width=50, yscrollcommand=song_scoll.set)
song_listbox.bind('<<ListboxSelect>>', curSongSelect)
song_listbox.grid(row=1)
song_scoll.config(command=song_listbox.yview)

artist_label = Label(window, text="Artist Name")
artist_label.grid(column=2, row=0)
artist_scoll = Scrollbar(window)
artist_scoll.grid(row=1, column=3, rowspan=10, sticky=N+S+W)
artist_listbox = Listbox(width=50, yscrollcommand=artist_scoll.set)
artist_listbox.bind('<<ListboxSelect>>', curArtistSelect)
artist_listbox.grid(row=1, column=2)
artist_scoll.config(command=artist_listbox.yview)

album_label = Label(window, text="Album Name")
album_label.grid(column=4, row=0)
album_scoll = Scrollbar(window)
album_scoll.grid(row=1, column=5, rowspan=10, sticky=N+S+W)
album_listbox = Listbox(width=50, yscrollcommand=album_scoll.set)
album_listbox.bind('<<ListboxSelect>>', curAlbumSelect)
album_listbox.grid(row=1, column=4)
album_scoll.config(command=album_listbox.yview)

collection_label = Label(window, text="Music Collection")
collection_label.grid(row=20, column= 2)
collection_scoll = Scrollbar(window)
collection_scoll.grid(row=21, column=5, rowspan=10, sticky=N+S+W)
collection_listbox = Listbox(width=160, yscrollcommand=collection_scoll.set)
# #collection_listbox.bind('<<ListboxSelect>>', curcollectionSelect)
collection_listbox.grid(row=21, column=0, columnspan=5)
collection_scoll.config(command=collection_listbox.yview)

song_var = StringVar()
artist_var = StringVar()
album_var = StringVar()

song_entry = Entry(window, textvariable=song_var)
song_entry.grid(row=10)

artist_entry = Entry(window, textvariable=artist_var)
artist_entry.grid(row=10, column=2)

album_entry = Entry(window, textvariable=album_var)
album_entry.grid(row=10, column=4)

song_button = Button(window, text="Search", command=getSongQuery)
song_button.grid(row=15)

artist_button = Button(window, text="Search", command=getArtistQuery)
artist_button.grid(row=15, column=2)

album_button = Button(window, text="Search", command=getAlbumQuery)
album_button.grid(row=15, column=4)

create_entry = Button(window, text="Add Entry", command=createEntry)
create_entry.grid(row=18, column=2)

window.mainloop()

