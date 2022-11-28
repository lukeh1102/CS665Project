import tkinter as tk
from tkinter import ttk
import sqlite3
import datetime
import time
import threading

conn = sqlite3.connect('data.db')
c = conn.cursor()



root = tk.Tk()
root.resizable(False, False)
root.title("Library Management System - CS665 Project")
root.configure(background = "#C0C0C0")

# Center Window
screenWidth = root.winfo_screenwidth()
screenHeight = root.winfo_screenheight()
ROOT_WINDOW_WIDTH = 800
ROOT_WINDOW_HEIGHT = 500
x = (screenWidth/2) - (ROOT_WINDOW_WIDTH/2)
y = (screenHeight/2) - (ROOT_WINDOW_HEIGHT/2)
root.geometry('%dx%d+%d+%d' % (ROOT_WINDOW_WIDTH, ROOT_WINDOW_HEIGHT, x, y))

# Widget Sizes
BUTTON_REL_WIDTH = 0.12
BUTTON_REL_HEIGHT = 0.08
NEW_WINDOW_WIDTH = 400
NEW_WINDOW_HEIGHT = 300

class Scrollable(ttk.Frame):
    """
       Make a frame scrollable with scrollbar on the right.
       After adding or removing widgets to the scrollable frame,
       call the update() method to refresh the scrollable area.
    """

    def __init__(self, frame, width=16):

        scrollbar = tk.Scrollbar(frame, width=width)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, expand=False)

        self.canvas = tk.Canvas(frame, yscrollcommand=scrollbar.set, background="white")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar.config(command=self.canvas.yview)

        self.canvas.bind('<Configure>', self.__fill_canvas)

        # base class initialization
        ttk.Frame.__init__(self, frame)

        # assign this obj (the inner frame) to the windows item of the canvas
        self.windows_item = self.canvas.create_window(0,0, window=self, anchor=tk.NW)


    def __fill_canvas(self, event):
        "Enlarge the windows item to the canvas width"

        canvas_width = event.width
        self.canvas.itemconfig(self.windows_item, width = canvas_width)

    def update(self):
        "Update the canvas and the scrollregion"

        self.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox(self.windows_item))

# Button Functions
def displayCheckedout(tableBody, scrollableBody):

    tableBody.destroy()
    scrollableBody.destroy()
    tableBody = ttk.Frame(root, style="TFrame")
    tableBody.place(relx=0.2, rely=0.05, relwidth=0.8, relheight=1)
    scrollableBody = Scrollable(tableBody)


    #join checkouts, members, and books tables to get checkout info
    c.execute("""SELECT checkouts.CheckoutID, checkouts.Book, books.Title, books.Author, checkouts.ReturnDate, members.Name, checkouts.CheckedoutBy   
    FROM checkouts
    INNER JOIN members ON checkouts.CheckedoutBy = members.MemberID
    INNER JOIN books ON checkouts.Book = books.BookID""")
    checkoutInfo = c.fetchall()

    #make style for label with white background
    style = ttk.Style()
    style.configure("white.TLabel", background="white")

    #display header
    headerLabel.config(text="Checked Out Books")

    #delete old widgets in scrollableBody
    for widget in scrollableBody.winfo_children():
        widget.destroy()
    scrollableBody.update()

    #display table headers
    checkoutIDLabel = ttk.Label(scrollableBody, text="Checkout ID", anchor="center", style="white.TLabel")
    # #checkoutIDLabel.place(relx=0.2, rely=0.05, relwidth=0.1, relheight=0.05)
    checkoutIDLabel.grid(row=0, column=0)

    bookIDLabel = ttk.Label(scrollableBody, text="Book ID", anchor="center", style="white.TLabel")
    # #bookIDLabel.place(relx=0.31, rely=0.05, relwidth=0.1, relheight=0.05)
    bookIDLabel.grid(row=0, column=1)

    bookTitleLabel = ttk.Label(scrollableBody, text="Book Title", anchor="center", style="white.TLabel")
    # #bookTitleLabel.place(relx=0.42, rely=0.05, relwidth=0.1, relheight=0.05)
    bookTitleLabel.grid(row=0, column=2)

    bookAuthorLabel = ttk.Label(scrollableBody, text="Book Author", anchor="center", style="white.TLabel")
    # #bookAuthorLabel.place(relx=0.53, rely=0.05, relwidth=0.1, relheight=0.05)
    bookAuthorLabel.grid(row=0, column=3)

    returnDateLabel = ttk.Label(scrollableBody, text="Return Date", anchor="center", style="white.TLabel")
    # #returnDateLabel.place(relx=0.64, rely=0.05, relwidth=0.1, relheight=0.05)
    returnDateLabel.grid(row=0, column=4, padx=10)

    memberNameLabel = ttk.Label(scrollableBody, text="Name", anchor="center", style="white.TLabel")
    # #memberNameLabel.place(relx=0.75, rely=0.05, relwidth=0.1, relheight=0.05)
    memberNameLabel.grid(row=0, column=5, padx=10)

    memberIDLabel = ttk.Label(scrollableBody, text="Member ID", anchor="center", style="white.TLabel")
    # #memberIDLabel.place(relx=0.86, rely=0.05, relwidth=0.1, relheight=0.05)
    memberIDLabel.grid(row=0, column=6, padx=10)

    scrollableBody.update()

    #display all checked out books
    y=1
    for row in checkoutInfo:
        # I don't think using .place works with scrollableBody
        checkoutID = ttk.Label(scrollableBody, text=row[0], style="white.TLabel")
        checkoutID.grid(row=y, column=0)

        bookID = ttk.Label(scrollableBody, text=row[1], style="white.TLabel")
        bookID.grid(row=y, column=1, padx=0)

        bookTitle = ttk.Label(scrollableBody, text=row[2], style="white.TLabel")
        bookTitle.grid(row=y, column=2, padx=0)

        bookAuthor = ttk.Label(scrollableBody, text=row[3], style="white.TLabel")
        bookAuthor.grid(row=y, column=3, padx=0)

        returnDate = ttk.Label(scrollableBody, text=row[4], style="white.TLabel")
        returnDate.grid(row=y, column=4, padx=10)

        memberName = ttk.Label(scrollableBody, text=row[5], style="white.TLabel")
        memberName.grid(row=y, column=5, padx=10)

        memberID = ttk.Label(scrollableBody, text=row[6], style="white.TLabel")
        memberID.grid(row=y, column=6, padx=10)
        
        #Anytime youre using a scrollable body, you need to call update() for the widgets to appear
        scrollableBody.update()

        y+=1

def browseGenre(tableBody, scrollableBody):

    def rbSelected(event):
        genre = genreVar.get()

        if genre == "Fiction":
            #join checkouts and books tables to get return date and fiction book id, book title, and book author
            c.execute("""SELECT books.BookID, books.Title, books.Author, books.Genre, checkouts.ReturnDate, checkouts.book
            FROM books
            LEFT JOIN checkouts ON books.BookID = checkouts.Book
            WHERE books.Genre = "Fiction" """)
            bookInfo = c.fetchall()
        elif genre == "Non-Fiction":
            #join checkouts and books tables to get return date and non-fiction book id, book title, and book author
            c.execute("""SELECT books.BookID, books.Title, books.Author, books.Genre, checkouts.ReturnDate, checkouts.book
            FROM books
            LEFT JOIN checkouts ON books.BookID = checkouts.Book
            WHERE books.Genre = "Non-Fiction" """)
            bookInfo = c.fetchall()
        elif genre == "Mystery":
            #join checkouts and books tables to get return date and mystery book id, book title, and book author
            c.execute("""SELECT books.BookID, books.Title, books.Author, books.Genre, checkouts.ReturnDate, checkouts.book
            FROM books
            LEFT JOIN checkouts ON books.BookID = checkouts.Book
            WHERE books.Genre = "Mystery" """)
            bookInfo = c.fetchall()
        elif genre == "Fantasy":
            #join checkouts and books tables to get return date and fantasy book id, book title, and book author
            c.execute("""SELECT books.BookID, books.Title, books.Author, books.Genre, checkouts.ReturnDate, checkouts.book
            FROM books
            LEFT JOIN checkouts ON books.BookID = checkouts.Book
            WHERE books.Genre = "Fantasy" """)
            bookInfo = c.fetchall()
        elif genre == "Sci-Fi":
            #join checkouts and books tables to get return date and sci-fi book id, book title, and book author
            c.execute("""SELECT books.BookID, books.Title, books.Author, books.Genre, checkouts.ReturnDate, checkouts.book
            FROM books
            LEFT JOIN checkouts ON books.BookID = checkouts.Book
            WHERE books.Genre = "Science Fiction" """)
            bookInfo = c.fetchall()
        elif genre == "Romance":
            #join checkouts and books tables to get return date and romance book id, book title, and book author
            c.execute("""SELECT books.BookID, books.Title, books.Author, books.Genre, checkouts.ReturnDate, checkouts.book
            FROM books
            LEFT JOIN checkouts ON books.BookID = checkouts.Book
            WHERE books.Genre = "Romance" """)
            bookInfo = c.fetchall()
        elif genre == "Horror":
            #join checkouts and books tables to get return date and horror book id, book title, and book author
            c.execute("""SELECT books.BookID, books.Title, books.Author, books.Genre, checkouts.ReturnDate, checkouts.book
            FROM books
            LEFT JOIN checkouts ON books.BookID = checkouts.Book
            WHERE books.Genre = "Horror" """)
            bookInfo = c.fetchall()
        elif genre == "Biography":
            #join checkouts and books tables to get return date and biography book id, book title, and book author
            c.execute("""SELECT books.BookID, books.Title, books.Author, books.Genre, checkouts.ReturnDate, checkouts.book
            FROM books
            LEFT JOIN checkouts ON books.BookID = checkouts.Book
            WHERE books.Genre = "Biography" """)
            bookInfo = c.fetchall()
        elif genre == "History":
            #join checkouts and books tables to get return date and history book id, book title, and book author
            c.execute("""SELECT books.BookID, books.Title, books.Author, books.Genre, checkouts.ReturnDate, checkouts.book
            FROM books
            LEFT JOIN checkouts ON books.BookID = checkouts.Book
            WHERE books.Genre = "History" """)
            bookInfo = c.fetchall()
        
        #delete old widgets in scrollableBody
        for widget in scrollableBody.winfo_children():
            widget.destroy()
        scrollableBody.update()

        #display table headers
        bookIDLabel = ttk.Label(scrollableBody, text="Book ID", anchor="center", style="white.TLabel")
        bookIDLabel.grid(row=0, column=0, padx=20)

        bookTitleLabel = ttk.Label(scrollableBody, text="Book Title", anchor="center", style="white.TLabel")
        bookTitleLabel.grid(row=0, column=1, padx=20)

        bookAuthorLabel = ttk.Label(scrollableBody, text="Book Author", anchor="center", style="white.TLabel")
        bookAuthorLabel.grid(row=0, column=2, padx=20)

        bookGenreLabel = ttk.Label(scrollableBody, text="Book Genre", anchor="center", style="white.TLabel")
        bookGenreLabel.grid(row=0, column=3, padx=20)

        returnDateLabel = ttk.Label(scrollableBody, text="Return Date", anchor="center", style="white.TLabel")
        returnDateLabel.grid(row=0, column=4, padx=20)

        #display all books
        y=1
        for row in bookInfo:
            bookIDLabel = ttk.Label(scrollableBody, text=row[0], style="white.TLabel")
            bookIDLabel.grid(row=y, column=0, padx=20)

            bookTitleLabel = ttk.Label(scrollableBody, text=row[1], style="white.TLabel")
            bookTitleLabel.grid(row=y, column=1, padx=20)

            bookAuthorLabel = ttk.Label(scrollableBody, text=row[2], style="white.TLabel")
            bookAuthorLabel.grid(row=y, column=2, padx=20)

            bookGenreLabel = ttk.Label(scrollableBody, text=row[3], style="white.TLabel")
            bookGenreLabel.grid(row=y, column=3, padx=20)

            if row[4] == None:
                returnDateLabel = ttk.Label(scrollableBody, text="Available", style="white.TLabel")
                returnDateLabel.grid(row=y, column=4, padx=20)
            else:
                returnDateLabel = ttk.Label(scrollableBody, text=row[4], style="white.TLabel")
                returnDateLabel.grid(row=y, column=4, padx=20)

            scrollableBody.update()

            y+=1

        print(bookInfo)
        if bookInfo == []:
            noBooksLabel = ttk.Label(scrollableBody, text="No books found", style="white.TLabel")
            noBooksLabel.grid(row=1, column=0)
            scrollableBody.update()


    tableBody.destroy()
    scrollableBody.destroy()
    tableBody = ttk.Frame(root, style="TFrame")
    tableBody.place(relx=0.2, rely=0.1, relwidth=0.8, relheight=1)
    scrollableBody = Scrollable(tableBody)
    
    headerLabel.config(text="Browse Books by Genre")

    #radio button frame
    boxFrame = ttk.Frame(root, style="TFrame")
    boxFrame.place(relx=0.2, rely=0.05, relwidth=0.8, relheight=0.05)

    style = ttk.Style()
    style.configure("white.TLabel", background="white")
        
    #join checkouts and books tables to get return date and all book id, book title, and book author
    c.execute("""SELECT books.BookID, books.Title, books.Author, books.Genre, checkouts.ReturnDate, checkouts.book
    FROM books
    LEFT JOIN checkouts ON books.BookID = checkouts.Book""")
    bookInfo = c.fetchall()

    #delete old widgets in scrollableBody
    for widget in scrollableBody.winfo_children():
        widget.destroy()
    scrollableBody.update()

    #display table headers
    bookIDLabel = ttk.Label(scrollableBody, text="Book ID", anchor="center", style="white.TLabel")
    bookIDLabel.grid(row=0, column=0, padx=20)

    bookTitleLabel = ttk.Label(scrollableBody, text="Book Title", anchor="center", style="white.TLabel")
    bookTitleLabel.grid(row=0, column=1, padx=20)

    bookAuthorLabel = ttk.Label(scrollableBody, text="Book Author", anchor="center", style="white.TLabel")
    bookAuthorLabel.grid(row=0, column=2, padx=20)

    bookGenreLabel = ttk.Label(scrollableBody, text="Book Genre", anchor="center", style="white.TLabel")
    bookGenreLabel.grid(row=0, column=3, padx=20)

    returnDateLabel = ttk.Label(scrollableBody, text="Return Date", anchor="center", style="white.TLabel")
    returnDateLabel.grid(row=0, column=4, padx=20)

    y=1
    for row in bookInfo:
        bookIDLabel = ttk.Label(scrollableBody, text=row[0], style="white.TLabel")
        bookIDLabel.grid(row=y, column=0, padx=20)

        bookTitleLabel = ttk.Label(scrollableBody, text=row[1], style="white.TLabel")
        bookTitleLabel.grid(row=y, column=1, padx=20)

        bookAuthorLabel = ttk.Label(scrollableBody, text=row[2], style="white.TLabel")
        bookAuthorLabel.grid(row=y, column=2, padx=20)

        bookGenreLabel = ttk.Label(scrollableBody, text=row[3], style="white.TLabel")
        bookGenreLabel.grid(row=y, column=3, padx=20)

        if row[4] == None:
            returnDateLabel = ttk.Label(scrollableBody, text="Available", style="white.TLabel")
            returnDateLabel.grid(row=y, column=4)
        else:
            returnDateLabel = ttk.Label(scrollableBody, text=row[4], style="white.TLabel")
            returnDateLabel.grid(row=y, column=4)

        scrollableBody.update()

        y+=1

    #Combo Box
    genreVar = tk.StringVar()
    genreVar.set("All")

    genreBox = ttk.Combobox(boxFrame, textvariable=genreVar)
    genreBox["values"] = ("All", "Fiction", "Non-Fiction", "Mystery", "Fantasy", "Sci-Fi", "Romance", "Horror", "Biography", "History")
    genreBox.current(0)
    genreBox.place(relx=0.4, rely=0.1, relwidth=0.2, relheight=0.8)

    # when a genre is selected, display all books in that genre
    genreBox.bind("<<ComboboxSelected>>", rbSelected)


def searchBook():

    def searchClicked():

        #if entry is empty ask for entry
        if searchBookEntry.get() == "":
            errorLabel.config(text="Please enter a MemberID")
            return

        #join books and checkouts tables to get book info
        c.execute("""SELECT books.BookID, books.Title, books.Author, books.Genre, checkouts.ReturnDate, checkouts.Book
        FROM books
        LEFT JOIN checkouts ON books.BookID = checkouts.Book
        WHERE books.BookID =?""", (searchBookEntry.get(),))

        #join books, authors, and genres tables to get book, title, author, and genre
        # c.execute("""SELECT books.BookID, books.Title, books.Author, books.Genre, authors.Name, genres.GenreName
        # FROM books 
        # INNER JOIN authors ON books.Author = authors.AuthorID
        # INNER JOIN genres ON books.Genre = genres.GenreID
        # WHERE books.Title LIKE ?""", (searchBookEntry.get(),))
        bookInfo = c.fetchall()

        #if book is not found, display error message
        if bookInfo == []:
            #make lavel text red style
            style = ttk.Style()
            style.configure("red.TLabel", foreground="red")
            errorLabel.config(text="Book not found", style="red.TLabel")
            return
        else:
            #update entry with book info
            #make entry modifiable again
            bookTitleEntry.config(state="normal")
            #clear entry
            bookTitleEntry.delete(0, tk.END)
            #insert new text
            bookTitleEntry.insert(0, bookInfo[0][1])
            #make entry unmodifiable
            bookTitleEntry.config(state="readonly")

            bookAuthorEntry.config(state="normal")
            bookAuthorEntry.delete(0, tk.END)
            bookAuthorEntry.insert(0, bookInfo[0][2])
            bookAuthorEntry.config(state="readonly")

            bookGenreEntry.config(state="normal")
            bookGenreEntry.delete(0, tk.END)
            bookGenreEntry.insert(0, bookInfo[0][3])
            bookGenreEntry.config(state="readonly")

            #if book is checked out, display return date
            if bookInfo[0][4] != None:
                checkedoutStatusLabel.config(text="Checkout Status: Due " + str(bookInfo[0][4]))
            else:
                checkedoutStatusLabel.config(text="Checkout Status: Available")

            #make edit button clickable
            editButton.config(state="normal")

    def editClicked():

        def cancelClicked():
            bookTitleEntry.delete(0,tk.END)
            bookAuthorEntry.delete(0,tk.END)
            bookGenreEntry.delete(0,tk.END)

            #set old values back
            bookTitleEntry.insert(0, oldTitle)
            bookAuthorEntry.insert(0, oldAuthor)
            bookGenreEntry.insert(0, oldGenre)

            #make entries unmodifiable
            bookTitleEntry.config(state="readonly")
            bookAuthorEntry.config(state="readonly")
            bookGenreEntry.config(state="readonly")

            #make search entry modifiable
            searchBookEntry.confi(state="normal")
                
            #make save and cancel buttons unclickable
            saveButton.config(state="disabled")
            cancelButton.config(state="disabled")

        #make save button clickable
        saveButton.config(state="normal")

        #make cancel button clickable
        cancelButton.config(state="normal")
        cancelButton.config(command=cancelClicked)

        #make entries unmodifiable
        searchBookEntry.config(state="readonly")

        #make entries modifiable
        bookTitleEntry.config(state="normal")
        bookAuthorEntry.config(state="normal")
        bookGenreEntry.config(state="normal")

        #save old values
        oldTitle = bookTitleEntry.get()
        oldAuthor = bookAuthorEntry.get()
        oldGenre = bookGenreEntry.get()

    def saveClicked():

        #get values
        bookID = searchBookEntry.get()
        newTitle = bookTitleEntry.get()
        newAuthor = bookAuthorEntry.get()
        newGenre = bookGenreEntry.get()

        #update book info
        c.execute("""UPDATE books SET Title = ?, Author = ?, Genre = ? WHERE BookID = ?""", (newTitle, newAuthor, newGenre, bookID))
        conn.commit()

        #make entries unmodifiable
        bookTitleEntry.config(state="readonly")
        bookAuthorEntry.config(state="readonly")
        bookGenreEntry.config(state="readonly")

        #make search entry modifiable
        searchBookEntry.config(state="normal")

        #make save and cancel buttons unclickable
        saveButton.config(state="disabled")
        cancelButton.config(state="disabled")

    #create new window
    searchBookWindow = tk.Toplevel(root)
    searchBookWindow.resizable(False, False)
    searchBookWindow.title("Search Book")
    searchBookWindow.grab_set()
    searchBookWindow.geometry('%dx%d+%d+%d' % (NEW_WINDOW_WIDTH, NEW_WINDOW_HEIGHT, x, y))

    #create widgets

    searchBookLabel = ttk.Label(searchBookWindow, text="BookID:", anchor="w")
    searchBookLabel.place(relx=0.1, rely=0.04, relwidth=1, relheight=0.05)

    searchBookEntry = ttk.Entry(searchBookWindow)
    searchBookEntry.place(relx=0.1, rely=0.1, relwidth=0.6, relheight=0.1)

    #widgets to display book info

    bookTitleLabel = ttk.Label(searchBookWindow, text="Title:", anchor="sw")
    bookTitleLabel.place(relx=0.1, rely=0.27, relwidth=0.2, relheight=0.05)

    bookTitleEntry = ttk.Entry(searchBookWindow)
    bookTitleEntry.place(relx=0.23, rely=0.25, relwidth=0.67, relheight=0.1)
    bookTitleEntry.config(state="readonly")

    bookAuthorLabel = ttk.Label(searchBookWindow, text="Author:", anchor="sw")
    bookAuthorLabel.place(relx=0.1, rely=0.39, relwidth=0.2, relheight=0.05)

    bookAuthorEntry = ttk.Entry(searchBookWindow)
    bookAuthorEntry.place(relx=0.23, rely=0.37, relwidth=0.67, relheight=0.1)
    bookAuthorEntry.config(state="readonly")

    bookGenreLabel = ttk.Label(searchBookWindow, text="Genre:", anchor="sw")
    bookGenreLabel.place(relx=0.1, rely=0.51, relwidth=0.2, relheight=0.05)

    bookGenreEntry = ttk.Entry(searchBookWindow)
    bookGenreEntry.place(relx=0.23, rely=0.49, relwidth=0.67, relheight=0.1)
    bookGenreEntry.config(state="readonly")

    checkedoutStatusLabel = ttk.Label(searchBookWindow, text="Checkout Status:", anchor="w")
    checkedoutStatusLabel.place(relx=0.1, rely=0.7, relwidth=0.8, relheight=0.1)

    errorLabel = ttk.Label(searchBookWindow, text="")
    errorLabel.place(relx=0.4, rely=0.85, relwidth=0.5, relheight=0.1)

    #buttons

    searchBookButton = ttk.Button(searchBookWindow, text="Search", command=searchClicked, takefocus=False)
    searchBookButton.place(relx=0.75, rely=0.1, relwidth=0.15, relheight=0.1)

    editButton = ttk.Button(searchBookWindow, text="Edit", command=editClicked, takefocus=False, state="disabled")
    editButton.place(relx=0.23, rely=0.6, relwidth=0.15, relheight=0.1)

    saveButton = ttk.Button(searchBookWindow, text="Update", command=saveClicked, takefocus=False, state="disabled")
    saveButton.place(relx=0.40, rely=0.6, relwidth=0.15, relheight=0.1)

    cancelButton = ttk.Button(searchBookWindow, text="Cancel", takefocus=False, state="disabled")
    cancelButton.place(relx=0.57, rely=0.6, relwidth=0.15, relheight=0.1)


def searchMember():

    def searchClicked():

        #if entry is empty ask for entry
        if searchMemberEntry.get() == "":
            errorLabel.config(text="Please enter a MemberID")
            return

        #join members, fines, and checkouts tables to get name, address, birthday, books, duedate, and fines
        c.execute("""SELECT members.Name, members.Address, members.Birthday, checkouts.Book, checkouts.Returndate, fines.FineAmount, books.Title, fines.IssuedTo
        FROM members LEFT JOIN checkouts ON members.MemberID = checkouts.CheckedoutBy 
        LEFT JOIN fines ON members.MemberID = fines.IssuedTo 
        LEFT JOIN books ON checkouts.Book = books.BookID
        WHERE members.MemberID = ?""", (searchMemberEntry.get(),))
        memberInfo = c.fetchall()

        # if member is not found, display error message
        if memberInfo == []:
            #make lavel text red style
            style = ttk.Style()
            style.configure("red.TLabel", foreground="red")
            errorLabel.config(text="Member not found", style="red.TLabel")
            return
        else:

            # update entry with member info
            # make entry modifable again
            memberNameEntry.config(state="normal")
            # clear entry
            memberNameEntry.delete(0, tk.END)
            # insert new text
            memberNameEntry.insert(0, memberInfo[0][0])
            # make entry unmodifable
            memberNameEntry.config(state="readonly")

            memberAddressEntry.config(state="normal")
            memberAddressEntry.delete(0, tk.END)
            memberAddressEntry.insert(0, memberInfo[0][1])
            memberAddressEntry.config(state="readonly")

            memberBirthdayEntry.config(state="normal")
            memberBirthdayEntry.delete(0, tk.END)
            memberBirthdayEntry.insert(0, memberInfo[0][2])
            memberBirthdayEntry.config(state="readonly")

            #add up all the fines
            totalFines = 0
            for row in memberInfo:
                if row[5] != None:
                    totalFines += row[5]
        
            fineLabel.config(text="Unpaid Fine Amount: $" + str(totalFines))

            #list books checked out
            checkedOutBooks = ""
            bookCheckedOut = False
            for row in memberInfo:
                if row[3] != None:
                    bookCheckedOut = True
                    checkedOutBooks += str(row[6]) + " Due: " + str(row[4]) + ", "
        
            if bookCheckedOut == True:
                booksLabel.config(text="Checked Out Books: " + checkedOutBooks)
            else:
                booksLabel.config(text="Checked Out Books: None")

            # make edit button clickable
            editButton.config(state="normal")

    def editClicked():

        def cancelClicked():
        
            #clear entry boxs
            memberNameEntry.delete(0, tk.END)
            memberAddressEntry.delete(0, tk.END)
            memberBirthdayEntry.delete(0, tk.END)

            #set old values back
            memberNameEntry.insert(0, oldName)
            memberAddressEntry.insert(0, oldAddress)
            memberBirthdayEntry.insert(0, oldBirthday)

            #make entries unmodifable
            memberNameEntry.config(state="readonly")
            memberAddressEntry.config(state="readonly")
            memberBirthdayEntry.config(state="readonly")

            #make search entry modifable
            searchMemberEntry.config(state="normal")

            #make save and cancel buttons unclickable
            saveButton.config(state="disabled")
            cancelButton.config(state="disabled")


        #make save button clickable
        saveButton.config(state="normal")

        #make cancel button clickable
        cancelButton.config(state="normal")
        cancelButton.config(command=cancelClicked)

        #make search entry unmodifable
        searchMemberEntry.config(state="readonly")

        #make entries modifable
        memberNameEntry.config(state="normal")
        memberAddressEntry.config(state="normal")
        memberBirthdayEntry.config(state="normal")

        #save old values
        oldName = memberNameEntry.get()
        oldAddress = memberAddressEntry.get()
        oldBirthday = memberBirthdayEntry.get()


    def saveClicked():
        
        # get values
        memberID = searchMemberEntry.get()
        newName = memberNameEntry.get()
        newAddress = memberAddressEntry.get()
        newBirthday = memberBirthdayEntry.get()

        #update member info
        c.execute("""UPDATE members SET Name = ?, Address = ?, Birthday = ? 
        WHERE MemberID = ?""", (newName, newAddress, newBirthday, memberID))
        conn.commit()

        #make entry unmodifable
        memberNameEntry.config(state="readonly")
        memberAddressEntry.config(state="readonly")
        memberBirthdayEntry.config(state="readonly")

        #make search entry modifable
        searchMemberEntry.config(state="normal")

        #make buttons unclickable
        saveButton.config(state="disabled")
        cancelButton.config(state="disabled")


    #create new window
    searchMemberWindow = tk.Toplevel(root)
    searchMemberWindow.resizable(False, False)
    searchMemberWindow.title("Search Member")
    searchMemberWindow.grab_set()
    searchMemberWindow.geometry('%dx%d+%d+%d' % (NEW_WINDOW_WIDTH, NEW_WINDOW_HEIGHT, x, y))

    #create widgets

    searchMemberLabel = ttk.Label(searchMemberWindow, text="MemberID:", anchor="w")
    searchMemberLabel.place(relx=0.1, rely=0.04, relwidth=1, relheight=0.05)

    searchMemberEntry = ttk.Entry(searchMemberWindow)
    searchMemberEntry.place(relx=0.1, rely=0.1, relwidth=0.6, relheight=0.1)

    #widgets to display member info

    memberNameLabel = ttk.Label(searchMemberWindow, text="Name:", anchor="sw")
    memberNameLabel.place(relx=0.1, rely=0.27, relwidth=0.2, relheight=0.05)

    memberNameEntry = ttk.Entry(searchMemberWindow)
    memberNameEntry.place(relx=0.23, rely=0.25, relwidth=0.67, relheight=0.1)
    memberNameEntry.config(state="readonly")

    memberAddressLabel = ttk.Label(searchMemberWindow, text="Address:", anchor="sw")
    memberAddressLabel.place(relx=0.1, rely=0.39, relwidth=0.2, relheight=0.05)

    memberAddressEntry = ttk.Entry(searchMemberWindow)
    memberAddressEntry.place(relx=0.23, rely=0.37, relwidth=0.67, relheight=0.1)
    memberAddressEntry.config(state="readonly")

    memberBirthdayLabel = ttk.Label(searchMemberWindow, text="Birthday:", anchor="sw")
    memberBirthdayLabel.place(relx=0.1, rely=0.51, relwidth=0.2, relheight=0.05)

    memberBirthdayEntry = ttk.Entry(searchMemberWindow)
    memberBirthdayEntry.place(relx=0.23, rely=0.49, relwidth=0.67, relheight=0.1)
    memberBirthdayEntry.config(state="readonly")


    fineLabel = ttk.Label(searchMemberWindow, text="Unpaid Fine Amount:", anchor="w")
    fineLabel.place(relx=0.1, rely=0.7, relwidth=0.8, relheight=0.1)

    booksLabel = ttk.Label(searchMemberWindow, text="Books Checked Out:", anchor="nw")
    booksLabel.place(relx=0.1, rely=0.78, relwidth=0.8, relheight=0.2)

    errorLabel = ttk.Label(searchMemberWindow, text="")
    errorLabel.place(relx=0.4, rely=0.85, relwidth=0.5, relheight=0.1)

    #buttons

    searchMemberButton = ttk.Button(searchMemberWindow, text="Search", command=searchClicked, takefocus=False)
    searchMemberButton.place(relx=0.75, rely=0.1, relwidth=0.15, relheight=0.1)

    editButton = ttk.Button(searchMemberWindow, text="Edit", command=editClicked, takefocus=False, state="disabled")
    editButton.place(relx=0.23, rely=0.6, relwidth=0.15, relheight=0.1)

    saveButton = ttk.Button(searchMemberWindow, text="Update", command=saveClicked, takefocus=False, state="disabled")
    saveButton.place(relx=0.40, rely=0.6, relwidth=0.15, relheight=0.1)

    cancelButton = ttk.Button(searchMemberWindow, text="Cancel", takefocus=False, state="disabled")
    cancelButton.place(relx=0.57, rely=0.6, relwidth=0.15, relheight=0.1)

def deleteItem():
    
    def renderDeleteItemWindow():

        def clearMessage(widget):
            time.sleep(3)
            widget.config(text="")

        def deleteFromDB():
            if selectedItem.get() == 1:
                # delete member
                newMemberID = memberIDEntry.get()

                confirmLabel = ttk.Label(deleteItemWindow, text="")
                confirmLabel.place(rely=0.775, relwidth=1, relheight=0.1)

                #check if entries are empty
                if newMemberID == "":
                    confirmLabel.config(text="Please fill out all fields")
                else:
                    #delete entry
                    c.execute("DELETE FROM members WHERE memberID = ?", (newMemberID,))
                    conn.commit()
                    
                    #provide user with a message to confirm entry
                    confirmLabel.config(text="Member deleted successfully")
                    #clear message after 3 seconds, needed to open a new thread to count while the GUI still runs
                    t = threading.Thread(target=clearMessage, args=(confirmLabel,))
                    t.start()

                    #clear entries
                    memberIDEntry.delete(0, 'end')

            if selectedItem.get() == 2:
                # delete book
                newBookID = bookIDEntry.get()

                confirmLabel = ttk.Label(deleteItemWindow, text="")
                confirmLabel.place(rely=0.775, relwidth=1, relheight=0.1)

                #check if entries are empty
                if newBookID == "":
                    confirmLabel.config(text="Please fill out all fields")
                else:
                    #delete entry
                    c.execute("DELETE FROM books WHERE bookID = ?", (newBookID,)) 
                    conn.commit()

                    #provide user with a message to confirm entry
                    confirmLabel.config(text="Book deleted successfully")
                    #clear message after 3 seconds, needed to open a new thread to count while the GUI still runs
                    t = threading.Thread(target=clearMessage, args=(confirmLabel,))
                    t.start()

                    #clear entries
                    bookIDEntry.delete(0, 'end')

            if selectedItem.get() == 3:
                # delete fine
                newFineID = fineIDEntry.get()

                confirmLabel = ttk.Label(deleteItemWindow, text="")
                confirmLabel.place(rely=0.775, relwidth=1, relheight=0.1)

                #check if entries are empty
                if newFineID == "":
                    confirmLabel.config(text="Please fill out all fields")
                else:
                    #delete entry
                    c.execute("DELETE FROM fines WHERE fineID = ?", (newFineID,))
                    conn.commit()

                    #provide user with a message to confirm entry
                    confirmLabel.config(text="Fine deleted successfully")
                    #clear message after 3 seconds, needed to open a new thread to count while the GUI still runs
                    t = threading.Thread(target=clearMessage, args=(confirmLabel,))
                    t.start()
                    
                    #clear entries
                    fineIDEntry.delete(0, 'end')

        for widget in renderFrame.winfo_children():
            widget.destroy()

        if selectedItem.get() == 1:

            memberIDLabel = ttk.Label(renderFrame, text="Member ID:", foreground="black", anchor="w")
            memberIDLabel.place(relx=0.05, rely=0, relwidth=1, relheight=0.1)

            memberIDEntry = ttk.Entry(renderFrame)
            memberIDEntry.place(relx = 0.05, rely = 0.1, relwidth = 0.8, relheight = 0.15)

        if selectedItem.get() == 2:

            bookIDLabel = ttk.Label(renderFrame, text="Book ID:", foreground="black", anchor="w")
            bookIDLabel.place(relx=0.05, rely=0, relwidth=1, relheight=0.1)

            bookIDEntry = ttk.Entry(renderFrame)
            bookIDEntry.place(relx = 0.05, rely = 0.1, relwidth = 0.8, relheight = 0.15)

        if selectedItem.get() == 3:

            fineIDLabel = ttk.Label(renderFrame, text="Fine ID:", foreground="black", anchor="w")
            fineIDLabel.place(relx=0.05, rely=0, relwidth=1, relheight=0.1)

            fineIDEntry = ttk.Entry(renderFrame)
            fineIDEntry.place(relx = 0.05, rely = 0.1, relwidth = 0.8, relheight = 0.15)

        deleteButton = ttk.Button(renderFrame, text="Delete", command=deleteFromDB)
        deleteButton.place(relx=0.4, rely=0.85, relwidth=0.2, relheight=0.1)    

    deleteItemWindow = tk.Toplevel(root)
    deleteItemWindow.title("Delete Item")
    deleteItemWindow.resizable(False, False)
    deleteItemWindow.grab_set()
    x = (screenWidth/2) - (NEW_WINDOW_WIDTH/2)
    y = (screenHeight/2) - (NEW_WINDOW_HEIGHT/2)
    deleteItemWindow.geometry('%dx%d+%d+%d' % (NEW_WINDOW_WIDTH, NEW_WINDOW_HEIGHT, x, y))
    selectedItem = tk.IntVar()

    radioButtonFrame = ttk.Frame(deleteItemWindow)
    radioButtonFrame.place(relx=0, rely=0, anchor="nw", relwidth=1, relheight=0.1)

    renderFrame = ttk.Frame(deleteItemWindow)
    renderFrame.place(relx=0, rely=0.1, anchor="nw", relwidth=1, relheight=0.9)

    memberRB = ttk.Radiobutton(radioButtonFrame, text="Member", variable=selectedItem, value=1, command=renderDeleteItemWindow)
    memberRB.place(relx=0.1, rely=0.1, relwidth=0.2, relheight=0.8)

    bookRB = ttk.Radiobutton(radioButtonFrame, text="Book", variable=selectedItem, value=2, command=renderDeleteItemWindow)
    bookRB.place(relx=0.4, rely=0.1, relwidth=0.2, relheight=0.8)

    movieRB = ttk.Radiobutton(radioButtonFrame, text="Fine", variable=selectedItem, value=3, command=renderDeleteItemWindow)
    movieRB.place(relx=0.7, rely=0.1, relwidth=0.2, relheight=0.8)

def addItem():

    def renderAddItemWindow():

        def clearMessage(widget):
            time.sleep(3)
            widget.config(text="")

        def addToDB():

            if selectedItem.get() == 1:
                # add member
                newName = nameEntry.get()
                newAddress = addressEntry.get()
                newBirthday = birthdayEntry.get()

                confirmLabel = ttk.Label(addItemWindow, text="")
                confirmLabel.place(rely=0.775, relwidth=1, relheight=0.1)

                #check if entries are empty
                if newName == "" or newAddress == "" or newBirthday == "":
                    confirmLabel.config(text="Please fill out all fields")
                else:
                    #insert entry
                    c.execute("INSERT INTO members (Name, Address, Birthday) VALUES (?, ?, ?)", (newName, newAddress, newBirthday))
                    conn.commit()
                    
                    #provide user with a message to confirm entry
                    confirmLabel.config(text="Member added successfully")
                    #clear message after 3 seconds, needed to open a new thread to count while the GUI still runs
                    t = threading.Thread(target=clearMessage, args=(confirmLabel,))
                    t.start()

                    #clear entries
                    nameEntry.delete(0, 'end')
                    addressEntry.delete(0, 'end')
                    birthdayEntry.delete(0, 'end')

            if selectedItem.get() == 2:
                # add book
                newTitle = titleEntry.get()
                newAuthor = authorEntry.get()
                newGenre = genreEntry.get()

                confirmLabel = ttk.Label(addItemWindow, text="")
                confirmLabel.place(rely=0.775, relwidth=1, relheight=0.1)

                #check if entries are empty
                if newTitle == "" or newAuthor == "" or newGenre == "":
                    confirmLabel.config(text="Please fill out all fields")
                else:
                    #insert entry
                    c.execute("INSERT INTO books (Title, Author, Genre) VALUES (?, ?, ?)", (newTitle, newAuthor, newGenre))
                    conn.commit()

                    #provide user with a message to confirm entry
                    confirmLabel.config(text="Book added successfully")
                    #clear message after 3 seconds, needed to open a new thread to count while the GUI still runs
                    t = threading.Thread(target=clearMessage, args=(confirmLabel,))
                    t.start()

                    #clear entries
                    titleEntry.delete(0, 'end')
                    authorEntry.delete(0, 'end')
                    genreEntry.delete(0, 'end')

            if selectedItem.get() == 3:
                # add fine
                newIssuedTo = issueEntry.get()
                newFineAmount = amountEntry.get()
                newDateIssued = datetime.datetime.now().strftime("%m/%d/%Y")

                confirmLabel = ttk.Label(addItemWindow, text="")
                confirmLabel.place(rely=0.775, relwidth=1, relheight=0.1)

                #check if entries are empty
                if newIssuedTo == "" or newFineAmount == "":
                    confirmLabel.config(text="Please fill out all fields")
                else:
                    #insert entry
                    c.execute("INSERT INTO fines (IssuedTo, FineAmount, DateIssued) VALUES (?, ?, ?)", (newIssuedTo, newFineAmount, newDateIssued))
                    conn.commit()

                    #provide user with a message to confirm entry
                    confirmLabel.config(text="Fine issued successfully")
                    #clear message after 3 seconds, needed to open a new thread to count while the GUI still runs
                    t = threading.Thread(target=clearMessage, args=(confirmLabel,))
                    t.start()
                    
                    #clear entries
                    issueEntry.delete(0, 'end')
                    amountEntry.delete(0, 'end')


        for widget in renderFrame.winfo_children():
            widget.destroy()

            style = ttk.Style()
            style.configure("white.TLabel", background="white")

        if selectedItem.get() == 1:

            nameLabel = ttk.Label(renderFrame, text="Name:", foreground="black", anchor="w", style="white.TLabel")
            nameLabel.place(relx=0.05, rely=0, relwidth=1, relheight=0.1)

            nameEntry = ttk.Entry(renderFrame)
            nameEntry.place(relx = 0.05, rely = 0.1, relwidth = 0.8, relheight = 0.15)

            addressLabel = ttk.Label(renderFrame, text="Address:", foreground="black", anchor="w")
            addressLabel.place(relx=0.05, rely=0.25, relwidth=1, relheight=0.1)

            addressEntry = ttk.Entry(renderFrame)
            addressEntry.place(relx = 0.05, rely = 0.35, relwidth = 0.8, relheight = 0.15)

            birthdayLabel = ttk.Label(renderFrame, text="Birthday:", foreground="black", anchor="w")
            birthdayLabel.place(relx=0.05, rely=0.5, relwidth=1, relheight=0.1)

            birthdayEntry = ttk.Entry(renderFrame)
            birthdayEntry.place(relx = 0.05, rely = 0.6, relwidth = 0.8, relheight = 0.15)

        if selectedItem.get() == 2:

            titleLabel = ttk.Label(renderFrame, text="Title:", foreground="black", anchor="w")
            titleLabel.place(relx=0.05, rely=0, relwidth=1, relheight=0.1)

            titleEntry = ttk.Entry(renderFrame)
            titleEntry.place(relx = 0.05, rely = 0.1, relwidth = 0.8, relheight = 0.15)

            authorLabel = ttk.Label(renderFrame, text="Author:", foreground="black", anchor="w")
            authorLabel.place(relx=0.05, rely=0.25, relwidth=1, relheight=0.1)

            authorEntry = ttk.Entry(renderFrame)
            authorEntry.place(relx = 0.05, rely = 0.35, relwidth = 0.8, relheight = 0.15)

            genreLabel = ttk.Label(renderFrame, text="Genre:", foreground="black", anchor="w")
            genreLabel.place(relx=0.05, rely=0.5, relwidth=1, relheight=0.1)

            genreEntry = ttk.Entry(renderFrame)
            genreEntry.place(relx = 0.05, rely = 0.6, relwidth = 0.8, relheight = 0.15)

        if selectedItem.get() == 3:

            issueLabel = ttk.Label(renderFrame, text="Issue fine to:", foreground="black", anchor="w")
            issueLabel.place(relx=0.05, rely=0, relwidth=1, relheight=0.1)

            issueEntry = ttk.Entry(renderFrame)
            issueEntry.place(relx = 0.05, rely = 0.1, relwidth = 0.8, relheight = 0.15)

            amountLabel = ttk.Label(renderFrame, text="Fine amount:", foreground="black", anchor="w")
            amountLabel.place(relx=0.05, rely=0.25, relwidth=1, relheight=0.1)

            amountEntry = ttk.Entry(renderFrame)
            amountEntry.place(relx = 0.05, rely = 0.35, relwidth = 0.8, relheight = 0.15)

        addButton = ttk.Button(renderFrame, text="Add", command=addToDB)
        addButton.place(relx=0.4, rely=0.85, relwidth=0.2, relheight=0.1)

    addItemWindow = tk.Toplevel(root)
    addItemWindow.title("Add Item")
    addItemWindow.resizable(False, False)
    addItemWindow.grab_set()
    x = (screenWidth/2) - (NEW_WINDOW_WIDTH/2)
    y = (screenHeight/2) - (NEW_WINDOW_HEIGHT/2)
    addItemWindow.geometry('%dx%d+%d+%d' % (NEW_WINDOW_WIDTH, NEW_WINDOW_HEIGHT, x, y))
    selectedItem = tk.IntVar()

    radioButtonFrame = ttk.Frame(addItemWindow)
    radioButtonFrame.place(relx=0, rely=0, anchor="nw", relwidth=1, relheight=0.1)

    renderFrame = ttk.Frame(addItemWindow)
    renderFrame.place(relx=0, rely=0.1, anchor="nw", relwidth=1, relheight=0.9)

    memberRB = ttk.Radiobutton(radioButtonFrame, text="Member", variable=selectedItem, value=1, command=renderAddItemWindow)
    memberRB.place(relx=0.1, rely=0.1, relwidth=0.2, relheight=0.8)

    bookRB = ttk.Radiobutton(radioButtonFrame, text="Book", variable=selectedItem, value=2, command=renderAddItemWindow)
    bookRB.place(relx=0.4, rely=0.1, relwidth=0.2, relheight=0.8)

    movieRB = ttk.Radiobutton(radioButtonFrame, text="Fine", variable=selectedItem, value=3, command=renderAddItemWindow)
    movieRB.place(relx=0.7, rely=0.1, relwidth=0.2, relheight=0.8)


def checkoutBook():
    
    def clearMessage(widget):
        time.sleep(3)
        widget.config(text="")

    def addToDB():

        member = memberEntry.get()
        bookID = bookIDEntry.get()
        #get date two weeks from now m/d/Y format
        returnDate = datetime.datetime.now() + datetime.timedelta(days=14)
        returnDate = returnDate.strftime("%m/%d/%Y")


        if bookID == "" or member == "":
            confirmLabel.config(text="Please fill out all fields")
        else:
            #check if book is already checked out
            c.execute("SELECT * FROM checkouts WHERE Book = ?", (bookID,))
            result = c.fetchall()
            if len(result) > 0:
                confirmLabel.config(text="Book is already checked out")
                return

            #check if book exists
            c.execute("SELECT * FROM books WHERE BookID = ?", (bookID,))
            result = c.fetchall()
            if len(result) == 0:
                confirmLabel.config(text="Book does not exist")
                return

            #check if member exists
            c.execute("SELECT * FROM members WHERE MemberID = ?", (member,))
            result = c.fetchall()
            if len(result) == 0:
                confirmLabel.config(text="Member does not exist")
                return

            #insert entry
            c.execute("INSERT INTO checkouts (CheckedoutBy, Book, ReturnDate) VALUES (?, ?, ?)", (member, bookID, returnDate))
            conn.commit()
                    
            #provide user with a message to confirm entry
            confirmLabel.config(text="Book checked out successfully")
            #clear message after 3 seconds, needed to open a new thread to count while the GUI still runs
            t = threading.Thread(target=clearMessage, args=(confirmLabel,))
            t.start()

            #clear entries
            memberEntry.delete(0, 'end')
            bookIDEntry.delete(0, 'end')

    checkOutWindow = tk.Toplevel(root)
    checkOutWindow.title("Check Out Book")
    checkOutWindow.resizable(False, False)
    checkOutWindow.grab_set()
    x = (screenWidth/2) - (NEW_WINDOW_WIDTH/2)
    y = (screenHeight/2) - (NEW_WINDOW_HEIGHT/2)
    checkOutWindow.geometry('%dx%d+%d+%d' % (NEW_WINDOW_WIDTH, NEW_WINDOW_HEIGHT, x, y))

    renderFrame = ttk.Frame(checkOutWindow)
    renderFrame.place(relx=0, rely=0.1, anchor="nw", relwidth=1, relheight=0.9)

    bookIDLabel = ttk.Label(renderFrame, text="Book ID:", foreground="black", anchor="w")
    bookIDLabel.place(relx=0.05, rely=0, relwidth=1, relheight=0.1)

    bookIDEntry = ttk.Entry(renderFrame)
    bookIDEntry.place(relx = 0.05, rely = 0.1, relwidth = 0.8, relheight = 0.15)

    memberLabel = ttk.Label(renderFrame, text="Member ID:", foreground="black", anchor="w")
    memberLabel.place(relx=0.05, rely=0.25, relwidth=1, relheight=0.1)

    memberEntry = ttk.Entry(renderFrame)
    memberEntry.place(relx = 0.05, rely = 0.35, relwidth = 0.8, relheight = 0.15)

    addButton = ttk.Button(renderFrame, text="Add", command=addToDB)
    addButton.place(relx=0.4, rely=0.85, relwidth=0.2, relheight=0.1)

    confirmLabel = ttk.Label(renderFrame, text="")
    confirmLabel.place(rely=0.775, relwidth=1, relheight=0.1)


def returnBook():

    def clearMessage(widget):
        time.sleep(3)
        widget.config(text="")

    def removeFromDB():
        bookID = bookIDEntry.get()
        
        confirmLabel.config(text="")
        if bookID == "":
            confirmLabel.config(text="Please fill out all fields")
        else:
            #if book is not checked out, return
            c.execute("SELECT * FROM checkouts WHERE Book = ?", (bookID,))
            result = c.fetchall()
            if len(result) == 0:
                confirmLabel.config(text="Book is not checked out")
                return
            s=ttk.Style().configure("TFrame", background="white")

            #if book is checked out, delete entry
            c.execute("DELETE FROM checkouts WHERE Book = ?", (bookID,))
            conn.commit()
            confirmLabel.config(text="Book has been checked back in")

            t = threading.Thread(target=clearMessage, args=(confirmLabel,))
            t.start()

            bookIDEntry.delete(0, 'end')


    returnWindow = tk.Toplevel(root)
    returnWindow.title("Check Out Book")
    returnWindow.resizable(False, False)
    returnWindow.grab_set()
    x = (screenWidth/2) - (NEW_WINDOW_WIDTH/2)
    y = (screenHeight/2) - (NEW_WINDOW_HEIGHT/2)
    returnWindow.geometry('%dx%d+%d+%d' % (NEW_WINDOW_WIDTH, NEW_WINDOW_HEIGHT, x, y))

    renderFrame = ttk.Frame(returnWindow)
    renderFrame.place(relx=0, rely=0.1, anchor="nw", relwidth=1, relheight=0.9)

    bookIDLabel = ttk.Label(renderFrame, text="Book ID:", foreground="black", anchor="w")
    bookIDLabel.place(relx=0.05, rely=0, relwidth=1, relheight=0.1)

    bookIDEntry = ttk.Entry(renderFrame)
    bookIDEntry.place(relx = 0.05, rely = 0.1, relwidth = 0.8, relheight = 0.15)

    addButton = ttk.Button(renderFrame, text="Add", command=removeFromDB)
    addButton.place(relx=0.4, rely=0.85, relwidth=0.2, relheight=0.1)

    confirmLabel = ttk.Label(renderFrame, text="")
    confirmLabel.place(rely=0.775, relwidth=1, relheight=0.1)


headerLabel = ttk.Label(root, text="", anchor="center", font=("TkDefaultFont", 16), style="white.TLabel")
headerLabel.place(relx=0.2, rely=0, relwidth=0.8, relheight=0.055)

s=ttk.Style().configure("TFrame", background="white")
tableBody = ttk.Frame(root, style="TFrame")
tableBody.place(relx=0.2, rely=0.05, relwidth=0.8, relheight=1)
scrollableBody = Scrollable(tableBody)

# Add item button
addItemButton = ttk.Button(root, text="Add Item", command=addItem, takefocus=False)
addItemButton.place(relx = 0.05, rely = 0.05, relwidth=BUTTON_REL_WIDTH, relheight=BUTTON_REL_HEIGHT)

# Delete item button
deleteItemButton = ttk.Button(root, text="Delete Item", command=deleteItem, takefocus=False)
deleteItemButton.place(relx = 0.05, rely = 0.15, relwidth=BUTTON_REL_WIDTH, relheight=BUTTON_REL_HEIGHT)

# Checkout book button
checkoutBookButton = ttk.Button(root, text="Checkout Book", command=checkoutBook, takefocus=False)
checkoutBookButton.place(relx = 0.05, rely = 0.25, relwidth=BUTTON_REL_WIDTH, relheight=BUTTON_REL_HEIGHT)

# Return book button
returnBookButton = ttk.Button(root, text="Return Book", command=returnBook, takefocus=False)
returnBookButton.place(relx = 0.05, rely = 0.35, relwidth=BUTTON_REL_WIDTH, relheight=BUTTON_REL_HEIGHT)

# Display all checked out books
s = ttk.Style()
s.configure('my.TButton', font=("TkDefaultFont", 8))
displayCheckedoutButton = ttk.Button(root, text="Checked Out List", command=lambda: displayCheckedout(tableBody, scrollableBody), style='my.TButton', takefocus=False)
displayCheckedoutButton.place(relx = 0.05, rely = 0.45, relwidth=BUTTON_REL_WIDTH, relheight=BUTTON_REL_HEIGHT)

# Search Member button
searchMemberButton = ttk.Button(root, text="Search Member", takefocus=False, command=searchMember)
searchMemberButton.place(relx = 0.05, rely = 0.55, relwidth=BUTTON_REL_WIDTH, relheight=BUTTON_REL_HEIGHT)

# Search Book button
searchBookButton = ttk.Button(root, text="Search Book", takefocus=False, command=searchBook)
searchBookButton.place(relx = 0.05, rely = 0.65, relwidth=BUTTON_REL_WIDTH, relheight=BUTTON_REL_HEIGHT)

displayCheckedoutButton = ttk.Button(root, text="Browse By Genre", command=lambda: browseGenre(tableBody, scrollableBody), style='my.TButton', takefocus=False)
displayCheckedoutButton.place(relx = 0.05, rely = 0.75, relwidth=BUTTON_REL_WIDTH, relheight=BUTTON_REL_HEIGHT)




root.mainloop()
