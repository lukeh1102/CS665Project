import sqlite3
import datetime

conn = sqlite3.connect('data.db')
c = conn.cursor()

# delete all data from tables

c.execute("DELETE FROM members")
c.execute("DELETE FROM books")
c.execute("DELETE FROM fines")
c.execute("DELETE FROM checkouts")
conn.commit()

#set sequence to 0 for each table
c.execute("UPDATE sqlite_sequence SET seq = 0 WHERE name = 'members'")
c.execute("UPDATE sqlite_sequence SET seq = 0 WHERE name = 'books'")
c.execute("UPDATE sqlite_sequence SET seq = 0 WHERE name = 'fines'")
c.execute("UPDATE sqlite_sequence SET seq = 0 WHERE name = 'checkouts'")
conn.commit()


#create lists of data to insert into tables
members = [('Luke Walker', '111 Main St', '11/02/2000'), ('Jennifer Siviseth', '222 Main St', '01/19/2002'), ('Nate Walker', '333 Main St', '06/07/2002'), ('Maya Miller', '444 Main St', '12/02/2000'),
            ('Bob Smith', '555 Main St', '03/12/2010'), ('Bob Doe', '666 Main St', '05/11/1995'), ('Sally Smith', '777 Main St', '09/08/2007'), ('Sally Doe', '888 Main St', '02/12/2001')]

books = [('The Hobbit', 'J.R.R. Tolkien', 'Fantasy'), ('The Lord of the Rings', 'J.R.R. Tolkien', 'Fantasy'), ('Eragon', 'Christopher Paolini', 'Fantasy'), ('The Hunger Games', 'Suzanne Collins', 'Science Fiction'),
            ('The Giver', 'Lois Lowry', 'Science Fiction'), ('The Maze Runner', 'James Dashner', 'Science Fiction'), ('The Fault in Our Stars', 'John Green', 'Romance'), ('The Notebook', 'Nicholas Sparks', 'Romance')]

fines = [(1, 5, '01/01/2022'), (2, 10, '01/01/2022'), (4, 5, '05/01/2022'), (4, 5, '06/01/2022'), (4, 15, '06/04/2022'), (8, 5, '07/01/2022'), (5, 5, '07/01/2018'), (3, 10, '11/01/2018')]

checkouts = [(1, 1, '12/01/2022'), (2, 2, '12/01/2022'), (3, 3, '12/04/2022'), (4, 4, '12/05/2022'), (5, 5, '12/11/2022'), (6, 6, '12/01/2022'), (7, 7, '12/07/2022'), (8, 8, '12/10/2022')]

#insert data into tables
c.executemany("INSERT INTO members(Name, Address, Birthday) VALUES(?, ?, ?)", members)
c.executemany("INSERT INTO books(Title, Author, Genre) VALUES(?, ?, ?)", books)
c.executemany("INSERT INTO fines(IssuedTo, FineAmount, DateIssued) VALUES(?, ?, ?)", fines)
c.executemany("INSERT INTO checkouts(CheckedoutBy, Book, ReturnDate) VALUES(?, ?, ?)", checkouts)
conn.commit()



