import csv

def countSongCollection(cursor):
    # finds the most popularly added songs
    query = "SELECT id, count(id) as count from collection group by id"
    cursor.execute(query)
    data = cursor.fetchall()
    print(data)

    with open('collection_song.csv', mode='w') as song_file:
        song_writer = csv.writer(song_file)
