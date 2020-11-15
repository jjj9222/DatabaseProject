import csv

def countSongCollection(cursor):
    # finds the most popularly added songs
    query = "SELECT s.id, r.title, count(s.id) as count " \
            "from \"songCollection\" s, song r " \
            "where s.id = r.id group by s.id, r.title"
    cursor.execute(query)
    data = cursor.fetchall()
    print(data)

    with open('collection_song.csv', mode='w') as song_file:
        fields = ['id', 'title', 'count']
        song_writer = csv.DictWriter(song_file, fieldnames=fields)
        song_writer.writeheader()

        for row in data:
            song_writer.writerow({fields[0]: row[0], fields[1]: row[1], fields[2]: row[2]})
