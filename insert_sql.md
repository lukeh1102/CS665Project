# Members Table
```sql
INSERT INTO members(Name, Address, Birthday) VALUES('Luke Walker', '111 Main St', '11/02/2000')
INSERT INTO members(Name, Address, Birthday) VALUES('Jennifer Siviseth', '222 Main St', '01/19/2002')
INSERT INTO members(Name, Address, Birthday) VALUES ('Nate Walker', '333 Main St', '06/07/2002')
INSERT INTO members(Name, Address, Birthday) VALUES('Maya Miller', '444 Main St', '12/02/2000')
INSERT INTO members(Name, Address, Birthday) VALUES('Bob Smith', '555 Main St', '03/12/2010')
INSERT INTO members(Name, Address, Birthday) VALUES('Bob Doe', '666 Main St', '05/11/1995')
INSERT INTO members(Name, Address, Birthday) VALUES('Sally Smith', '777 Main St', '09/08/2007')
INSERT INTO members(Name, Address, Birthday) VALUES('Sally Doe', '888 Main St', '02/12/2001')
```

# Books Table
```sql
INSERT INTO books(Title, Author, Genre) VALUES('The Hobbit', 'J.R.R. Tolkien', 'Fantasy')
INSERT INTO books(Title, Author, Genre) VALUES('The Lord of the Rings', 'J.R.R. Tolkien', 'Fantasy')
INSERT INTO books(Title, Author, Genre) VALUES('Eragon', 'Christopher Paolini', 'Fantasy')
INSERT INTO books(Title, Author, Genre) VALUES('The Hunger Games', 'Suzanne Collins', 'Science Fiction')
INSERT INTO books(Title, Author, Genre) VALUES('The Giver', 'Lois Lowry', 'Science Fiction')
INSERT INTO books(Title, Author, Genre) VALUES('The Maze Runner', 'James Dashner', 'Science Fiction')
INSERT INTO books(Title, Author, Genre) VALUES('The Fault in Our Stars', 'John Green', 'Romance')
INSERT INTO books(Title, Author, Genre) VALUES('The Notebook', 'Nicholas Sparks', 'Romance')
```

# Fines Table
```sql
INSERT INTO fines(IssuedTo, FineAmount, DateIssued) VALUES(1, 5, '01/01/2022')
INSERT INTO fines(IssuedTo, FineAmount, DateIssued) VALUES(2, 10, '01/01/2022')
INSERT INTO fines(IssuedTo, FineAmount, DateIssued) VALUES(4, 5, '05/01/2022')
INSERT INTO fines(IssuedTo, FineAmount, DateIssued) VALUES(4, 5, '06/01/2022')
INSERT INTO fines(IssuedTo, FineAmount, DateIssued) VALUES(4, 15, '06/04/2022')
INSERT INTO fines(IssuedTo, FineAmount, DateIssued) VALUES(8, 30, '07/01/2022')
INSERT INTO fines(IssuedTo, FineAmount, DateIssued) VALUES(5, 35, '07/01/2018')
INSERT INTO fines(IssuedTo, FineAmount, DateIssued) VALUES(3, 40, '11/01/2018')
```

# Checkoust Table
```sql
INSERT INTO checkouts(CheckedoutBy, Book, ReturnDate) VALUES(1, 1, '12/01/2022')
INSERT INTO checkouts(CheckedoutBy, Book, ReturnDate) VALUES(2, 2, '12/01/2022')
INSERT INTO checkouts(CheckedoutBy, Book, ReturnDate) VALUES(3, 3, '12/04/2022')
INSERT INTO checkouts(CheckedoutBy, Book, ReturnDate) VALUES(4, 4, '12/05/2022')
INSERT INTO checkouts(CheckedoutBy, Book, ReturnDate) VALUES(5, 5, '12/11/2022')
INSERT INTO checkouts(CheckedoutBy, Book, ReturnDate) VALUES(6, 6, '12/01/2022')
INSERT INTO checkouts(CheckedoutBy, Book, ReturnDate) VALUES(7, 7, '12/07/2022')
INSERT INTO checkouts(CheckedoutBy, Book, ReturnDate) VALUES(8, 8, '12/10/2022')
```