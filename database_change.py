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


    # Elif statement used to display all songs when user enters * or nothing
    # across the other lists, corresponding artist and albums will be displayed if a song is created by one or a song is in album
    if (song_var.get() == "*" or song_var.get() == ""):
        cursor.execute("""SELECT title from song""")
        data = cursor.fetchall()
        for row in data:
            song_listbox.insert(END, row[0])


        #display all artists that sing songs, all albums that have songs in them
        query = "SELECT DISTINCT A.\"firstName\", A.\"lastName\" from artist A, song S, performed P where P.\"artistID\" = A.\"artistID\" AND P.id = S.id"
        cursor.execute(query)
        data = cursor.fetchall()
        artist_listbox.delete(0, END)
        for row in data:
            artist_listbox.insert(END, row)

        query = "SELECT DISTINCT A.\"albumName\" from album A, song S, contains C where A.\"albumID\" = C.\"albumID\" AND C.id = S.id"
        cursor.execute(query)
        data = cursor.fetchall()
        album_listbox.delete(0, END)
        for row in data:
            album_listbox.insert(END, row[0])

    # Else statement is for refined searches
    # a user can enter text and a query will be populated
    else:
        try:
            query = "SELECT id from song where title like '%" + song_var.get() + "%'"
            cursor.execute(query)
            song_ids = cursor.fetchall()
        except:
            print("Failed to get song IDs")
        try:
            query = "SELECT title from song where title like '%" + song_var.get() + "%'"
            cursor.execute(query)
            data = cursor.fetchall()
            for row in data:
                song_listbox.insert(END, row[0])
        except:
            print("Invalid Query")

        try:
            artist_listbox.delete(0, END)
            for number in song_ids:
                query = "SELECT DISTINCT A.\"firstName\", A.\"lastName\" from artist A, song S, performed P where P.\"artistID\" = A.\"artistID\" AND P.id = {0[0]}".format(number)
                cursor.execute(query)
                data = cursor.fetchall()
                for row in data:
                    artist_listbox.insert(END, row[0])
        except:
            print("Error")

        try:
            album_listbox.delete(0, END)
            for number in song_ids:
                query = "SELECT DISTINCT A.\"albumName\" from album A, song S, contains C where A.\"albumID\" = C.\"albumID\" AND C.id = {0[0]}".format(number)
                cursor.execute(query)
                data = cursor.fetchall()
                for row in data:
                    album_listbox.insert(END, row[0])
        except:
            print("Error")


def getArtistQuery():
    # Deletes the info in the listbox on press of button
    artist_listbox.delete(0, END)

    if (artist_var.get() == "*" or artist_var.get() == ""):
        cursor.execute("""SELECT "firstName", "lastName" from artist""")
        data = cursor.fetchall()
        for row in data:
            artist_listbox.insert(END, row)

        # display all songs that an artist sings, all albums that have artist in them
        query = "SELECT DISTINCT S.title from artist A, song S, performed P where P.\"artistID\" = A.\"artistID\" AND P.id = S.id"
        cursor.execute(query)
        data = cursor.fetchall()
        song_listbox.delete(0, END)
        for row in data:
            song_listbox.insert(END, row[0])

        query = "SELECT DISTINCT A.\"albumName\" from album A, artist S, produced P where A.\"albumID\" = P.\"albumID\" AND P.\"artistID\" = S.\"artistID\""
        cursor.execute(query)
        data = cursor.fetchall()
        album_listbox.delete(0, END)
        for row in data:
            album_listbox.insert(END, row[0])
    else:
        artistName = []
        try:
            if(artist_var.get()[0] == "("):
                artistName = artist_var.get()[1:len(artist_var.get())-1].split(',')
                i = 0
                while i < len(artistName):
                    artistName[i] = artistName[i].replace(" ", "")
                    artistName[i] = artistName[i].replace("\'", "")
                    i += 1
            if (len(artistName) > 0):
                query = "SELECT \"firstName\", \"lastName\" from artist where \"firstName\" like '%" + artistName[0] + "%' AND \"lastName\" like '%" + artistName[1] + "%'"
            else:
                query = "SELECT \"firstName\", \"lastName\" from artist where \"firstName\" like '%" + artist_var.get() + "%' or \"lastName\" like '%" + artist_var.get() + "%'"
            cursor.execute(query)
            data = cursor.fetchall()
            for row in data:
                artist_listbox.insert(END, row)
        except:
            print("Invalid Query")


        # Grab the artist id for use to compare to the relationship tables
        if (len(artistName) != 0):
            query = "SELECT \"artistID\" from artist where \"firstName\" like '%" + artistName[
                0] + "%' AND \"lastName\" like '%" + artistName[1] + "%'"
        else:
            query = "SELECT \"artistID\" from artist where \"firstName\" like '%" + artist_var.get() + "%' or \"lastName\" like '%" + artist_var.get() + "%'"
        cursor.execute(query)
        artist_ids = cursor.fetchall()

        try:
            # displaying the songs that the artists sing
            song_listbox.delete(0, END)
            for number in artist_ids:
                query = "SELECT DISTINCT S.title from song S, performed P where S.id = P.id AND P.\"artistID\" = {0[0]}".format(number)
                cursor.execute(query)
                data = cursor.fetchall()
                for row in data:
                    song_listbox.insert(END, row[0])
        except:
            print("Error")

        try:
            # displaying the albums that the artists make
            album_listbox.delete(0, END)
            for number in artist_ids:
                query = "SELECT DISTINCT A.\"albumName\" from album A, produced P where A.\"albumID\" = P.\"albumID\" AND P.\"artistID\" = {0[0]}".format(number)
                cursor.execute(query)
                data = cursor.fetchall()
                for row in data:
                    album_listbox.insert(END, row[0])
        except:
            print("Error")

def getAlbumQuery():
    # Deletes the info in the listbox on press of button
    album_listbox.delete(0, END)

    if (album_var.get() == "*" or album_var.get() == ""):
        cursor.execute("""SELECT "albumName" from album""")
        data = cursor.fetchall()
        for row in data:
            album_listbox.insert(END, row[0])

        # display all songs that are in albums
        query = "SELECT DISTINCT S.title from album A, song S, contains C where C.\"albumID\" = A.\"albumID\" AND C.id = S.id"
        cursor.execute(query)
        data = cursor.fetchall()
        song_listbox.delete(0, END)
        for row in data:
            song_listbox.insert(END, row[0])

        #display all artists that have an album
        query = "SELECT DISTINCT A.\"firstName\", A.\"lastName\" from artist A, album S, produced P where P.\"artistID\" = A.\"artistID\" AND P.\"albumID\" = S.\"albumID\""
        cursor.execute(query)
        data = cursor.fetchall()
        artist_listbox.delete(0, END)
        for row in data:
            artist_listbox.insert(END, row)


    else:
        # get a list of the album ID for comparison
        try:
            query = "SELECT \"albumID\" from album where \"albumName\" like '%" + album_var.get() + "%'"
            cursor.execute(query)
            album_ids = cursor.fetchall()
        except:
            print("Failed to get album IDs")

        try:
            query = "SELECT \"albumName\" from album where \"albumName\" like '%" + album_var.get() + "%'"
            cursor.execute(query)
            data = cursor.fetchall()
            for row in data:
                album_listbox.insert(END, row[0])
        except:
            print("Invalid Query")

        #Display the songs that are in a given album
        try:
            song_listbox.delete(0, END)
            for number in album_ids:
                query = "SELECT DISTINCT S.title from song S, contains C where S.id = C.id AND C.\"albumID\" = {0[0]}".format(number)
                cursor.execute(query)
                data = cursor.fetchall()
                for row in data:
                    song_listbox.insert(END, row[0])
        except:
            print("Error")

        #Display artist that was made the given album
        try:
            artist_listbox.delete(0, END)
            for number in album_ids:
                query = "SELECT DISTINCT A.\"firstName\", A.\"lastName\" from artist A, produced P where P.\"artistID\" = A.\"artistID\" AND P.\"albumID\" = {0[0]}".format(number)
                cursor.execute(query)
                data = cursor.fetchall()
                for row in data:
                    artist_listbox.insert(END, row[0])
        except:
            print("Error")



def curSongSelect(event):
    widget = event.widget
    cursor_select = widget.curselection()
    try:
        song_var.set(widget.get(cursor_select[0]))
    except:
        pass

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


def collectionEntry():

    #authenticate user
    if(user_var.get() != ""):
        query = "SELECT DISTINCT uid from \"user\" where username = \'" + user_var.get() + "\'"
        cursor.execute(query)
        user_id = cursor.fetchall()
        if (user_id != ""):
            if(song_var.get() != ""):
                try:
                    query = "SELECT DISTINCT id from song where title like '%" + song_var.get() + "%'"
                    cursor.execute(query)
                    ids = cursor.fetchall()
                    for song_id in ids:
                        query = "SELECT \"collectionID\" from collection where \'" + str(song_id[0]) + "\' = id AND \'" + str(user_id[0][0]) + "\' = uid"
                        cursor.execute(query)
                        repeat = cursor.fetchall()
                        if(len(repeat) != 0):
                            pass
                        else:
                            query = "INSERT INTO collection (id, uid) VALUES (\'" + str(song_id[0]) + "\', \'" + str(user_id[0][0]) + "\')"
                            cursor.execute(query)
                            update_collection()
                            query = "SELECT \"collectionID\" from collection where \'" + str(song_id[0]) + "\' = id AND \'" + str(user_id[0][0]) + "\' = uid"
                            cursor.execute(query)
                            coll_ID = cursor.fetchall()
                            query = "INSERT INTO \"songCollection\" (id, \"collectionID\") VALUES (\'" + str(song_id[0]) + "\', \'" + str(coll_ID[0][0]) + "\')"
                            cursor.execute(query)
                            update_collection()
                except:
                    print("error adding to collection", query)

            #ARTIST SECTION
            if (artist_var.get() != ""):
                artistName = []
                try:
                    if (artist_var.get()[0] == "("):
                        artistName = artist_var.get()[1:len(artist_var.get()) - 1].split(',')
                        i = 0
                        while i < len(artistName):
                            artistName[i] = artistName[i].replace(" ", "")
                            artistName[i] = artistName[i].replace("\'", "")
                            i += 1
                    if (len(artistName) > 0):
                        query = "SELECT \"artistID\" from artist where \"firstName\" like '%" + artistName[0] + "%' AND \"lastName\" like '%" + artistName[1] + "%'"
                    else:
                        query = "SELECT \"artistID\" from artist where \"firstName\" like '%" + artist_var.get() + "%' or \"lastName\" like '%" + artist_var.get() + "%'"

                    cursor.execute(query)
                    ids = cursor.fetchall()
                    for artist_id in ids:
                        query = "SELECT \"collectionID\" from collection where \'" + str(artist_id[0]) + "\' = \"artistID\" AND \'" + str(user_id[0][0]) + "\' = uid"
                        cursor.execute(query)
                        repeat = cursor.fetchall()
                        if (len(repeat) != 0):
                            pass
                        else:
                            query = "INSERT INTO collection (\"artistID\", uid) VALUES (\'" + str(artist_id[0]) + "\', \'" + str(user_id[0][0]) + "\')"
                            cursor.execute(query)
                            update_collection()
                            query = "SELECT \"collectionID\" from collection where \'" + str(artist_id[0]) + "\' = \"artistID\" AND \'" + str(user_id[0][0]) + "\' = uid"
                            cursor.execute(query)
                            coll_ID = cursor.fetchall()
                            query = "INSERT INTO \"artistCollection\" (\"artistID\", \"collectionID\") VALUES (\'" + str(artist_id[0]) + "\', \'" + str(coll_ID[0][0]) + "\')"
                            cursor.execute(query)
                            update_collection()
                except:
                    print("error adding to collection")


            # ALBUM SECTION
            if (album_var.get() != ""):
                try:
                    query = "SELECT \"albumID\" from album where \"albumName\" like '%" + album_var.get() + "%'"
                    cursor.execute(query)
                    ids = cursor.fetchall()
                    for album_id in ids:
                        query = "SELECT \"collectionID\" from collection where \'" + str(album_id[0]) + "\' = \"albumID\" AND \'" + str(user_id[0][0]) + "\' = uid"
                        cursor.execute(query)
                        repeat = cursor.fetchall()
                        if (len(repeat) != 0):
                            pass
                        else:
                            query = "INSERT INTO collection (\"albumID\", uid) VALUES (\'" + str(album_id[0]) + "\', \'" + str(user_id[0][0]) + "\')"
                            cursor.execute(query)
                            update_collection()
                            query = "SELECT \"collectionID\" from collection where \'" + str(album_id[0]) + "\' = \"albumID\" AND \'" + str(user_id[0][0]) + "\' = uid"
                            cursor.execute(query)
                            coll_ID = cursor.fetchall()
                            query = "INSERT INTO \"albumCollection\" (\"albumID\", \"collectionID\") VALUES (\'" + str(album_id[0]) + "\', \'" + str(coll_ID[0][0]) + "\')"
                            cursor.execute(query)
                            update_collection()
                except:
                    print("error adding to collection")

def update_collection():

    # remove previous list being displayed
    ca_listbox.delete(0, END)
    cs_listbox.delete(0, END)
    cal_listbox.delete(0, END)

    if(user_var.get() != ""):
        query = "SELECT DISTINCT uid from \"user\" where username = \'" + user_var.get() + "\'"
        cursor.execute(query)
        user_id = str(cursor.fetchall()[0][0])
        connection.commit()

        #update song collection list
        cursor.execute("SELECT DISTINCT S.title from song S, collection C where S.id = C.id AND C.uid = \'" + user_id + "\'")
        data = cursor.fetchall()
        for row in data:
            cs_listbox.insert(END, row[0])

        #update artist collection list
        cursor.execute("SELECT DISTINCT A.\"firstName\", A.\"lastName\" from artist A, collection C where A.\"artistID\" = C.\"artistID\"AND C.uid = \'" + user_id + "\'")
        data = cursor.fetchall()
        for row in data:
            ca_listbox.insert(END, row)

        cursor.execute("SELECT DISTINCT A.\"albumName\" from album A, collection C where A.\"albumID\" = C.\"albumID\"AND C.uid = \'" + user_id + "\'")
        data = cursor.fetchall()
        for row in data:
            cal_listbox.insert(END, row[0])


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

cs_label = Label(window, text="Music Collection")
cs_label.grid(row=20, column= 0)
cs_scoll = Scrollbar(window)
cs_scoll.grid(row=21, column=1, rowspan=10, sticky=N+S+W)
cs_listbox = Listbox(width=50, yscrollcommand=cs_scoll.set)
# #collection_listbox.bind('<<ListboxSelect>>', curcollectionSelect)
cs_listbox.grid(row=21, column=0)
cs_scoll.config(command=cs_listbox.yview)

ca_label = Label(window, text="Artist Collection")
ca_label.grid(row=20, column= 2)
ca_scoll = Scrollbar(window)
ca_scoll.grid(row=21, column=3, rowspan=10, sticky=N+S+W)
ca_listbox = Listbox(width=50, yscrollcommand=ca_scoll.set)
# #collection_listbox.bind('<<ListboxSelect>>', curcollectionSelect)
ca_listbox.grid(row=21, column=2)
ca_scoll.config(command=ca_listbox.yview)

cal_label = Label(window, text="Album Collection")
cal_label.grid(row=20, column= 4)
cal_scoll = Scrollbar(window)
cal_scoll.grid(row=21, column=5, rowspan=10, sticky=N+S+W)
cal_listbox = Listbox(width=50, yscrollcommand=cal_scoll.set)
# #collection_listbox.bind('<<ListboxSelect>>', curcollectionSelect)
cal_listbox.grid(row=21, column=4)
cal_scoll.config(command=cal_listbox.yview)

song_var = StringVar()
artist_var = StringVar()
album_var = StringVar()
user_var = StringVar()

song_entry = Entry(window, textvariable=song_var)
song_entry.grid(row=10)

artist_entry = Entry(window, textvariable=artist_var)
artist_entry.grid(row=10, column=2)

album_entry = Entry(window, textvariable=album_var)
album_entry.grid(row=10, column=4)

user_label = Label(window, text="Enter Username")
user_label.grid(row=24, column= 2)
user_entry = Entry(window, textvariable=user_var)
user_entry.grid(row=25, column=2)

song_button = Button(window, text="Search", command=getSongQuery)
song_button.grid(row=15)

artist_button = Button(window, text="Search", command=getArtistQuery)
artist_button.grid(row=15, column=2)

album_button = Button(window, text="Search", command=getAlbumQuery)
album_button.grid(row=15, column=4)

collection_entry = Button(window, text="Add Selection to Collection", command=collectionEntry)
collection_entry.grid(row=18, column=2)

display_button = Button(window, text="Display Collection", command=update_collection)
display_button.grid(row=26, column=2)

window.mainloop()
connection.close()

