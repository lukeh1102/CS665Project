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

## List checkedout books
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

# Delete