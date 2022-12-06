# **Library Management System**
Our database is modeled after a library management system, this system tracks the card holding members,  what books the library has, what books are checked out, and any outstanding fines.

With this application you can:  
- Add and remove members or books from the system
- Checkout and return books
- Search for books
- Manage fines
        

# Relations
Members(MemberID, Name, Address, Birthday)  
Books(BookID, Title, Author, Genre)  
Checkedout(CheckoutID, Book, CheckedoutBy, ReturnDate)  
Fines(FineID, IssuedTo, FineAmount, DateIssued)

# Tables - Examples
## Members
| MemberID |       Name        |   Address    |  Birthday  |
| :------: | :---------------: | :----------: | :--------: |
|    1     | Jennifer Siviseth | 111 Rocky Rd | 01/19/2001 |
|    2     |    Luke Walker    | 123 Easy St  | 11/02/2000 |

## Books
| BookID |       Title       |       Author        |  Genre  |
| :----: | :---------------: | :-----------------: | :-----: |
|   1    | Lord of The Rings |    J.R.R Tolkien    | Fantasy |
|   2    |      Eragon       | Chirstopher Paolini | Fantasy |


## CheckoutList
| CheckoutID | Book  | CheckedoutBy | ReturnDate |
| :--------: | :---: | :----------: | :--------: |
|     1      | B123  |   F234J457   | 11/29/2022 |
|     2      | B456  |   B843K735   | 11/23/2022 |

## Fines
| FineID | IssuedTo | FineAmount | DateIssued |
| :----: | :------: | :--------: | :--------: |
|   1    | F839G234 |     5      |  11/12/22  |
|   2    | L239P238 |     15     |  11/23/22  |

# FD's
## Members 
    MemberID->Name  
    MamberID->Address  
    MemberID->Birthday  
## Books
    BookID->Title  
    BookID->Author  
    BookID->Genre 
## Checkedout  
    CheckoutID->Book
    CheckoutID->CheckedoutBy
    CheckoutID->ReturnDate
## Fines
    FineID->IssuedTo
    FineID->FineAmount
    FineID->DateIssued

# Keys
## Primary Keys  
    MemberID  
    BookID  
    CheckoutID  
    FineID

## Foreign Keys  
    Checkedout(Book) references Books(BookID)
    Checkedout(CheckedoutBy) references Members(MemberID)
    Fines(IssuedTo) references Members(MemberID)
