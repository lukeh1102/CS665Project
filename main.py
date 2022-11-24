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

        self.canvas = tk.Canvas(frame, yscrollcommand=scrollbar.set)
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
    tableBody = ttk.Frame(root)
    tableBody.place(relx=0.2, rely=0.1, relwidth=0.8, relheight=1)
    scrollableBody = Scrollable(tableBody)

    #get all checked out books
    c.execute("SELECT * FROM checkouts")
    checkedOutBooks = c.fetchall()

    #display header
    headerLabel = ttk.Label(root, text="Checked Out Books", anchor="center", font=("TkDefaultFont", 16))
    headerLabel.place(relx=0.2, rely=0, relwidth=0.8, relheight=0.05)

    #display table headers
    checkoutIDLabel = ttk.Label(root, text="Checkout ID", anchor="center")
    checkoutIDLabel.place(relx=0.2, rely=0.05, relwidth=0.2, relheight=0.05)

    bookLabel = ttk.Label(root, text="Book ID", anchor="center")
    bookLabel.place(relx=0.4, rely=0.05, relwidth=0.2, relheight=0.05)

    checkedoutByLabel = ttk.Label(root, text="Checked Out By", anchor="center")
    checkedoutByLabel.place(relx=0.6, rely=0.05, relwidth=0.2, relheight=0.05)

    dueDateLabel = ttk.Label(root, text="Due Date", anchor="center")
    dueDateLabel.place(relx=0.8, rely=0.05, relwidth=0.2, relheight=0.05)
    


    #display all checked out books
    y=0
    for row in checkedOutBooks:

        # ttk.Label(scrollableBody, text=row[0]).place(x=0, y=y, width=160, height=50)
        # ttk.Label(scrollableBody, text=row[1]).place(relx=160, y=y, width=160, height=50)
        # ttk.Label(scrollableBody, text=row[2]).place(relx=320, y=y, width=160, height=50)
        # ttk.Label(scrollableBody, text=row[3]).place(relx=480, y=y, width=160, height=50)

        # Had to use trial and error to get the padding right for these
        # I don't think using .place works with scrollableBody
        CheckoutID = ttk.Label(scrollableBody, text=row[0])
        CheckoutID.grid(row=row[0], column=0, padx=70)

        book = ttk.Label(scrollableBody, text=row[1])
        book.grid(row=row[0], column=1, padx=40)

        checkedoutBy = ttk.Label(scrollableBody, text=row[2])
        checkedoutBy.grid(row=row[0], column=2, padx=30)

        dueDate = ttk.Label(scrollableBody, text=row[3])
        dueDate.grid(row=row[0], column=3, padx=70)

        #Anytime youre using a scrollable body, you need to call update() for the widgets to appear
        scrollableBody.update()



def addItem():

    def renderAddItemWindow():

        def clearMessage(widget):
            time.sleep(3)
            widget.config(text="")

        def addToDB():
            pass
            # TODO
            # Here is where the sql commands would go to add the item to the database
            # Commands would need to depend on radio button selection
            # Need to add error handling for if the user doesn't enter a value or value is already in db
            # ItemID(M### or B###) and MemberID(U###) should be auto generated

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



# Add item button
addItemButton = ttk.Button(root, text="Add Item", command=addItem, takefocus=False)
addItemButton.place(relx = 0.05, rely = 0.05, relwidth=BUTTON_REL_WIDTH, relheight=BUTTON_REL_HEIGHT)

# Delete item button
deleteItemButton = ttk.Button(root, text="Delete Item", takefocus=False)
deleteItemButton.place(relx = 0.05, rely = 0.15, relwidth=BUTTON_REL_WIDTH, relheight=BUTTON_REL_HEIGHT)

# Checkout book button
checkoutBookButton = ttk.Button(root, text="Checkout Item", takefocus=False)
checkoutBookButton.place(relx = 0.05, rely = 0.25, relwidth=BUTTON_REL_WIDTH, relheight=BUTTON_REL_HEIGHT)

# Return book button
returnBookButton = ttk.Button(root, text="Return Item", takefocus=False)
returnBookButton.place(relx = 0.05, rely = 0.35, relwidth=BUTTON_REL_WIDTH, relheight=BUTTON_REL_HEIGHT)


# Display all checked out books
s = ttk.Style()
s.configure('my.TButton', font=("TkDefaultFont", 8))
displayCheckedoutButton = ttk.Button(root, text="Checked Out List", command=displayCheckedout, style='my.TButton', takefocus=False)
displayCheckedoutButton.place(relx = 0.05, rely = 0.45, relwidth=BUTTON_REL_WIDTH, relheight=BUTTON_REL_HEIGHT)



#TODO 
# Buttons for searching for items
# Buttons for other pre-defined queries
# A frame that will display tables and search results






root.mainloop()
