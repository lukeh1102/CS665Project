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
def displayCheckedout():
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
    headerLabel = ttk.Label(root, text="Checked Out Books", anchor="center", font=("TkDefaultFont", 16))
    headerLabel.place(relx=0.2, rely=0, relwidth=0.8, relheight=0.05)

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
    returnDateLabel.grid(row=0, column=4)

    memberNameLabel = ttk.Label(scrollableBody, text="Name", anchor="center", style="white.TLabel")
    # #memberNameLabel.place(relx=0.75, rely=0.05, relwidth=0.1, relheight=0.05)
    memberNameLabel.grid(row=0, column=5)

    memberIDLabel = ttk.Label(scrollableBody, text="Member ID", anchor="center", style="white.TLabel")
    # #memberIDLabel.place(relx=0.86, rely=0.05, relwidth=0.1, relheight=0.05)
    memberIDLabel.grid(row=0, column=6)

    scrollableBody.update()

    #display all checked out books
    y=1
    for row in checkoutInfo:

        # ttk.Label(scrollableBody, text=row[0]).place(x=0, y=y, width=160, height=50)
        # ttk.Label(scrollableBody, text=row[1]).place(relx=160, y=y, width=160, height=50)
        # ttk.Label(scrollableBody, text=row[2]).place(relx=320, y=y, width=160, height=50)
        # ttk.Label(scrollableBody, text=row[3]).place(relx=480, y=y, width=160, height=50)

        # Had to use trial and error to get the padding right for these
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
        returnDate.grid(row=y, column=4, padx=0)

        memberName = ttk.Label(scrollableBody, text=row[5], style="white.TLabel")
        memberName.grid(row=y, column=5, padx=0)

        memberID = ttk.Label(scrollableBody, text=row[6], style="white.TLabel")
        memberID.grid(row=y, column=6, padx=0)
        
        #Anytime youre using a scrollable body, you need to call update() for the widgets to appear
        scrollableBody.update()

        y+=1

def searchMember():

    def searchClicked():

        #if entry is empty ask for entry
        if searchMemberEntry.get() == "":
            return

        #join members, fines, and checkouts tables to get name, address, birthday, books, duedate, and fines
        c.execute("""SELECT members.Name, members.Address, members.Birthday, checkouts.Book, checkouts.Returndate, fines.FineAmount, books.Title, fines.IssuedTo
        FROM members LEFT JOIN checkouts ON members.MemberID = checkouts.CheckedoutBy 
        LEFT JOIN fines ON members.MemberID = fines.IssuedTo 
        LEFT JOIN books ON checkouts.Book = books.BookID
        WHERE members.MemberID = ?""", (searchMemberEntry.get(),))
        memberInfo = c.fetchall()

        # if member is not found, display error message
        if memberInfo == None:
            return

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

    #buttons

    searchMemberButton = ttk.Button(searchMemberWindow, text="Search", command=searchClicked, takefocus=False)
    searchMemberButton.place(relx=0.75, rely=0.1, relwidth=0.15, relheight=0.1)

    editButton = ttk.Button(searchMemberWindow, text="Edit", command=editClicked, takefocus=False, state="disabled")
    editButton.place(relx=0.23, rely=0.6, relwidth=0.15, relheight=0.1)

    saveButton = ttk.Button(searchMemberWindow, text="Update", command=saveClicked, takefocus=False, state="disabled")
    saveButton.place(relx=0.40, rely=0.6, relwidth=0.15, relheight=0.1)

    cancelButton = ttk.Button(searchMemberWindow, text="Cancel", takefocus=False, state="disabled")
    cancelButton.place(relx=0.57, rely=0.6, relwidth=0.15, relheight=0.1)

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
                newDateIssued = datetime.datetime.now().strftime("%Y-%m-%d")

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


                

                #check if name is already in db
                #Forgot name is not actually unique, but we'll need this code later for other tables so I'm commenting it out for now
                # c.execute("SELECT Name FROM members WHERE Name = ?", (newName,))
                # if c.fetchone() is not None:
                #     nameLabel.config(text="Name already in database", foreground="red")
                # else:
                #     c.execute("INSERT INTO members (Name, Address, Birthday) VALUES (?, ?, ?)", (newName, newAddress, newBirthday))
                #     conn.commit()

                #     nameLabel.config(text="Name", foreground="black")
                #     confirmLabel = ttk.Label(addItemWindow, text="Member Added")
                #     confirmLabel.place(relx=0.4, rely=0.65, relwidth=0.2, relheight=0.15)

        for widget in renderFrame.winfo_children():
            widget.destroy()

        if selectedItem.get() == 1:

            nameLabel = ttk.Label(renderFrame, text="Name:", foreground="black", anchor="w")
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

#def checkout
#checkout window (book)
#book ID, member ID, return date (auto generated)

def checkOut():
    
    def clearMessage(widget):
        time.sleep(3)
        widget.config(text="")

    def addToDB():

        member = memberEntry.get()
        bookID = bookIDEntry.get()
        returnDate = datetime.datetime.now() + datetime.timedelta(days=14)

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

#def returnItem
#returnItem window
#memberID, bookID, return date

def returnItem():

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

s=ttk.Style().configure("TFrame", background="white")
tableBody = ttk.Frame(root, style="TFrame")
tableBody.place(relx=0.2, rely=0.05, relwidth=0.75, relheight=0.90)

# Add item button
addItemButton = ttk.Button(root, text="Add Item", command=addItem, takefocus=False)
addItemButton.place(relx = 0.05, rely = 0.05, relwidth=BUTTON_REL_WIDTH, relheight=BUTTON_REL_HEIGHT)

# Delete item button
deleteItemButton = ttk.Button(root, text="Delete Item", takefocus=False)
deleteItemButton.place(relx = 0.05, rely = 0.15, relwidth=BUTTON_REL_WIDTH, relheight=BUTTON_REL_HEIGHT)

# Checkout book button
checkoutBookButton = ttk.Button(root, text="Checkout Item", command=checkOut, takefocus=False)
checkoutBookButton.place(relx = 0.05, rely = 0.25, relwidth=BUTTON_REL_WIDTH, relheight=BUTTON_REL_HEIGHT)

# Return book button
returnBookButton = ttk.Button(root, text="Return Item", command=returnItem, takefocus=False)
returnBookButton.place(relx = 0.05, rely = 0.35, relwidth=BUTTON_REL_WIDTH, relheight=BUTTON_REL_HEIGHT)

# Display all checked out books
s = ttk.Style()
s.configure('my.TButton', font=("TkDefaultFont", 8))
displayCheckedoutButton = ttk.Button(root, text="Checked Out List", command=displayCheckedout, style='my.TButton', takefocus=False)
displayCheckedoutButton.place(relx = 0.05, rely = 0.45, relwidth=BUTTON_REL_WIDTH, relheight=BUTTON_REL_HEIGHT)

# Search Member button
searchMemberButton = ttk.Button(root, text="Search Member", takefocus=False, command=searchMember)
searchMemberButton.place(relx = 0.05, rely = 0.55, relwidth=BUTTON_REL_WIDTH, relheight=BUTTON_REL_HEIGHT)




#TODO 
# Buttons for searching for items
# Buttons for other pre-defined queries
# Buttons for filling table






root.mainloop()
