import csv
import time
import datetime

def countSongCollection(cursor):
    # finds the most popularly added songs
    query = "SELECT s.id, r.title, count(s.id) as count " \
            "from \"songCollection\" s, song r " \
            "where s.id = r.id group by s.id, r.title " \
            "order by count desc"
    cursor.execute(query)
    data = cursor.fetchall()
    print(data)

    with open('collection_song.csv', mode='w') as song_file:
        fields = ['id', 'title', 'count']
        song_writer = csv.DictWriter(song_file, fieldnames=fields)
        song_writer.writeheader()

        count = 0
        for row in data:
            if count == 10:
                break
            song_writer.writerow({fields[0]: row[0], fields[1]: row[1], fields[2]: row[2]})
            count += 1


def averageUserTime(cursor):
    # finds the average time users spend on the application
    today = datetime.datetime.today()
    formatToday = today.strftime('%Y-%m-%d')
    weekDays = [formatToday]
    dictWeek = {}
    avg = 0
    ct = 0
    for i in range(1, 7):
        weekday = today - datetime.timedelta(days=i)
        formatToday = weekday.strftime('%Y-%m-%d')
        weekDays.append(formatToday)

    for week in weekDays:
        query = "select l.uid, avg(s.length) as avg " \
                "from listens_to l, song s " \
                "where timestamp like \'%" + week + "%\' AND l.id = s.id " \
                                                           "group by l.uid"
        cursor.execute(query)
        data = cursor.fetchall()

        for row in data:
            if row[0] in dictWeek.keys():
                dictWeek[row[0]] += row[1]
            else:
                dictWeek[row[0]] = row[1]

    for key in dictWeek.keys():
        val = dictWeek[key]/420
        ct += 1
        avg += val
