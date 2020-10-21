from __future__ import print_function
import psycopg2
from tkinter import *
import time

hostname = 'reddwarf.cs.rit.edu'
username = 'p320_02'
password = 'Eux5iothoo3WaeL7yahM'
database = 'p320_02'

empty = True

# create connection to db
myConn = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)

# create initial window
top = Tk()
top.title("Music Player")
top.geometry("300x300")

query_var = StringVar()


def doQuery(conn, query_in):
    """
    execute query entered by user
    :param conn: connection to db
    :param query_in: sql query as entered by user
    """

    global empty
    empty = False
    if query_in == "":
        error = Label(top, text="Cannot execute empty query")
        error.grid(row=2, column=0)
        time.sleep(3)
        exit()
    cur = conn.cursor()
    cur.execute(query_in)

    for elem in cur.fetchall():
        displayQuery(elem)


def getQuery():
    global query_var
    global empty

    if not empty:
        lb.delete(0, END)
        empty = True

    query = query_var.get()

    doQuery(myConn, query)

    print(query)


def displayQuery(elem):
    index = 1
    r = 3
    lb.insert(index, elem)
    lb.grid(row=r)
    index += 1
    r += 1


# elements of the window
lab = Label(top, text="Enter query")
lab.grid(row=0, pady=5, padx=2)
q = Entry(top, textvariable=query_var)
q.grid(row=1, pady=5, padx=2)
but = Button(top, text="execute query", command=getQuery)
but.grid(row=2, pady=5, padx=2)
scroll = Scrollbar(top)
scroll.grid(row=3, column=1, rowspan=4, sticky=N+S+W)

lb = Listbox(top, yscrollcommand=scroll.set)
scroll.config(command=lb.yview)

top.mainloop()
myConn.close()


