# **Library Management System**
Our database is modeled after a library management system, this system tracks the card holding members,  
what books the library has, book checkout history, and a waiting list.

With this application you can:  
- Add and remove members or books from the system
- Checkout and return books
- Manage waitlist
- Search for books
        

# Relations
Members(MemberID, Name, Address, Birthday)  
Books(BookID, Title, Author, IsCheckedOut)  
CheckoutList(CheckoutID, BookID, MemberID, DateCheckedOut, ReturnDate)  
Waitlist(RequestID, BookID, MemberID, DateRequested)

# Tables - Examples
## Members
| MemberID |       Name        |   Address    |  Birthday  |
| :------: | :---------------: | :----------: | :--------: |
| F837M338 | Jennifer Siviseth | 111 Rocky Rd | 01/19/2001 |
| B843K735 |    Luke Walker    | 123 Easy St  | 11/02/2001 |

## Books
| BookID |       Title       |       Author        |  Genre  |
| :----: | :---------------: | :-----------------: | :-----: |
|  B123  | Lord of The Rings |    J.R.R Tolkien    | Fantasy |
|  B456  |      Eragon       | Chirstopher Paolini | Fantasy |


## CheckoutList
| CheckoutID | BookID | MemberID | ReturnDate |
| :--------: | :----- | :------: | :--------: |
|   C20576   | B123   | F234J457 | 11/29/2022 |
|   C67219   | B456   | B843K735 | 11/23/2022 |

## Waitlist
| RequestID |    Title    | MemberID | DateRequested |
| :-------: | :---------: | :------: | :-----------: |
|  R11111   | Animal Farm | A924Y539 |  11/17/2022   |
|  R22222   | Enders Game   | G347T259 |  11/23/2022   |
 

# FD's
## Members 
    MemberID->Name  
    MamberID->Address  
    MemberID->Birthday  
## Books
    BookID->Title  
    BookID->Author  
    BookID->Genre 
## CheckoutList  
    CheckoutID->BookID
    CheckoutID->MemberID
    CheckoutID->ReturnDate
## Waitlist
    RequestID->BookID
    RequestID->MemberID
    RequestID->DateRequested

# Keys
## Primary Keys  
    MemberID  
    BookID  
    CheckoutID  
    RequestID

## Foreign Keys/Constraints  
    ItemID->[MovieID,BookID]  
    CheckedOutBy->MemberID