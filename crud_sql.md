# Create
## Add items
```sql
INSERT INTO members (Name, Address, Birthday) VALUES (?, ?, ?), (newName, newAddress, newBirthday)
```
```sql
INSERT INTO books (Title, Author, Genre) VALUES (?, ?, ?), (newTitle, newAuthor, newGenre)
```
```sql
INSERT INTO fines (IssuedTo, FineAmount, DateIssued) VALUES (?, ?, ?), (newIssuedTo, newFineAmount, newDateIssued)
```
```sql
INSERT INTO checkouts (CheckedoutBy, Book, ReturnDate) VALUES (?, ?, ?), (newCheckedutBy, newBook, newReturnDate)
```


# Read
## Search member
```sql
SELECT members.Name, members.Address, members.Birthday, checkouts.Book, checkouts.Returndate, fines.FineAmount 
FROM members 
LEFT JOIN checkouts ON members.MemberID = checkouts.CheckedoutBy 
LEFT JOIN fines ON members.MemberID = fines.IssuedTo 
WHERE members.MemberID = ?, (searchMemberEntry.get(),)
```
```sql
SELECT books.BookID, books.Title, books.Author, books.Genre, checkouts.ReturnDate, checkouts.Book
FROM books
LEFT JOIN checkouts ON books.BookID = checkouts.Book
WHERE books.BookID = ?, (searchBookEntry.get(),)
```
## Search Book
```sql
SELECT books.BookID, books.Title, books.Author, books.Genre, checkouts.ReturnDate, checkouts.Book
FROM books
LEFT JOIN checkouts ON books.BookID = checkouts.Book
WHERE books.BookID =?
```
## Browse books by genre
When browsing books show all books by deafault
```sql
SELECT books.BookID, books.Title, books.Author, books.Genre, checkouts.ReturnDate, checkouts.book
FROM books
LEFT JOIN checkouts ON books.BookID = checkouts.Book
```
The query below is repeated several more times with other genres
```sql
SELECT books.BookID, books.Title, books.Author, books.Genre, checkouts.ReturnDate, checkouts.book
FROM books
LEFT JOIN checkouts ON books.BookID = checkouts.Book
WHERE books.Genre = "Fiction"
```


## List checked out books
```sql
SELECT checkouts.CheckoutID, checkouts.ReturnDate, members.Name, checkouts.CheckedoutBy, books.Title, books.Author, checkouts.Book
FROM checkouts
INNER JOIN members ON checkouts.CheckedoutBy = members.MemberID
INNER JOIN books ON checkouts.Book = books.BookID
```

# Update
## Update member information
```sql
UPDATE members SET Name = ?, Address = ?, Birthday = ? 
WHERE MemberID = ?, (newName, newAddress, newBirthday, memberID)
```
```sql
UPDATE books SET Title = ?, Author = ?, Genre = ? WHERE BookID = ?, (newTitle, newAuthor, newGenre, bookID)
```
## Update book information
```sql
UPDATE books SET Title = ?, Author = ?, Genre = ? WHERE BookID = ?, (newTitle, newAuthor, newGenre, bookID)
```

# Delete
## Delete itms
```sql
DELETE FROM fines WHERE fineID = ?, (newFineID,)
```
```sql
DELETE FROM books WHERE bookID = ?, (newBookID,)
```
```sql
DELETE FROM members WHERE memberID = ?, (newMemberID,)
```
```sql
DELETE FROM checkouts WHERE Book = ?, (bookID,)
```