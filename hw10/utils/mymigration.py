import json
import sqlite3
from datetime import datetime


def readjson(jfile):
    with open(jfile, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print("file: "+ jfile + " loaded")
    return data


def seed_auth():
    authors = readjson("authors.json")
    auth = []
    for a in authors:
        auth.append((a["fullname"], a["born_date"], a["born_location"], a["description"], datetime.now()))

    with sqlite3.connect('db.sqlite3') as con:
        cur = con.cursor()
        sql_authors = """INSERT INTO quotes_author(fullname, born_date, born_location, description, created_at) VALUES (?, ?, ?, ?, ?)"""
        cur.executemany(sql_authors, auth)
        con.commit() 


def seed_tags():
    quotes = readjson("qoutes.json")
    ts = set()

    for q in quotes:
        qt = q["tags"]
        for t in qt:
            ts.add((t, ))
    print(list(ts))

    with sqlite3.connect('db.sqlite3') as con:
        cur = con.cursor()
        sql_tags = """INSERT INTO quotes_tag(name) VALUES (?)"""
        cur.executemany(sql_tags, list(ts))
        con.commit() 


def read_authors():
    with sqlite3.connect('db.sqlite3') as con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM quotes_author;")
        return cur.fetchall()
    

def read_tags():
    with sqlite3.connect('db.sqlite3') as con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM quotes_tag;")
        return cur.fetchall()
    

def read_quote():
    with sqlite3.connect('db.sqlite3') as con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM quotes_quote;")
        return cur.fetchall()
    

def seed_quotes():
    authors = read_authors()

    def get_author(name):
        for a in authors:
            if name == a[1]:
                return a[0]
        return 0 

    quotes = readjson("qoutes.json")
    quot = []
    for q in quotes:
        quot.append((q["quote"], datetime.now(), get_author(q["author"])))

    with sqlite3.connect('db.sqlite3') as con:
        cur = con.cursor()
        sql_quotes = """INSERT INTO quotes_quote(quote, created_at, author_id) VALUES (?, ?, ?)"""
        cur.executemany(sql_quotes, quot)
        con.commit() 
            

def seed_quotes_tag():
    tags = read_tags()
    tagsdict = {}
    for t in tags:
        tagsdict[t[1]] = t[0]   # name: id

    index = 1
    quotes = readjson("qoutes.json")
    qtag = []
    for q in quotes:
        qt = q["tags"]
        for t in qt:
            qtag.append((index, tagsdict.get(t, 0)))
        index += 1 

    with sqlite3.connect('db.sqlite3') as con:
        cur = con.cursor()
        sql_qtag = """INSERT INTO quotes_quote_tag(quote_id, tag_id) VALUES (?, ?)"""
        cur.executemany(sql_qtag, qtag)
        con.commit() 


def seed_django():
    seed_auth()
    seed_tags()
    seed_quotes()
    seed_quotes_tag()
        
seed_django()
