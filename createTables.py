import sqlite3
import datetime

conn = sqlite3.connect('data.db')
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS 
members(
    MemberID integer PRIMARY KEY AUTOINCREMENT, 
    Name text NOT NULL, 
    Address text NOT NULL, 
    Birthday date NOT NULL)""")

c.execute("""CREATE TABLE IF NOT EXISTS 
books(
    BookID integer PRIMARY KEY AUTOINCREMENT,
    Title text NOT NULL,
    Author text NOT NULL,
    Genre text NOT NULL)""")

c.execute("""CREATE TABLE IF NOT EXISTS
fines(
    FineID integer PRIMARY KEY AUTOINCREMENT,
    IssuedTo integer NOT NULL,
    FineAmount integer NOT NULL,
    DateIssued date NOT NULL,
    FOREIGN KEY (IssuedTo) REFERENCES members(MemberID))""")

c.execute("""CREATE TABLE IF NOT EXISTS
checkouts(
    CheckoutID integer PRIMARY KEY AUTOINCREMENT,
    CheckedoutBy integer NOT NULL,
    Book integer NOT NULL,
    CheckoutDate date NOT NULL,
    FOREIGN KEY (CheckedoutBy) REFERENCES members(MemberID),
    FOREIGN KEY (Book) REFERENCES books(BookID))""")


    
