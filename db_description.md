# Library Service

Member(MemberId, Name, CanCheckOut, Birthday)  
Book(ItemID, Title, Author, Checkout)  
Movie(ItemID, Title, Director, CheckedOut)  
CheckedOutList(Title, ItemID, ReturnData, CheckedOutBy)  

# Tables - Examples
| Member     | 
|------------|

MemberID: F837M338, B843A735  
Name: Jennifer Siviseth, LuKe Walker  
CanCheckOut: True, False   
Birthday: 01/19/2001, 01/20/2001

| Book       | 
|------------|

BookID: B1, B2  
BookTitle: Narnia, Harry Potter  
Author: John Doe, Spongebob Squarepants  
BookCheckedOut: True, False 

| Movie      | 
|------------|

MovieID: M1, M2  
MovieTitle: John Wick, Matrix  
Director: Patrick Star, Mary Lee  
MovieCheckedOut: True, False

| CheckedOutList| 
|------------|

ItemID: B1, M1  
Title: Matrix, Narnia   
ReturnDate: 06/22/2023, 07/13/2023  
CheckedOutBy: Jennifer Siviseth, Luke Walker  

# FD's
Member 
- 
MemberID->Name  
MamberID->CanCheckOut  
MemberID->Birthday  

Book
-
BookID->BookTitle  
BookID->Author  
BookID->BookCheckedOut  

Movie  
-
MovieID->MovieTitle  
MovieID->Director  
MovieID->MovieCheckedOut  

CheckedOutList  
-
ItemID->Title  
ItemID->ReturnDate  
ItemID->CheckedOutBy

# Keys
Primary Keys  
-
* MemberID  
* BookID  
* MovieID  
* ItemID  

Foreign Keys/ Constraints
-
ItemID->[MovieID,BookID]  
CheckedOutBy->MemberID