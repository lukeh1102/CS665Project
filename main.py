import tkinter as tk
import sqlite3


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
NEW_WINDOW_HEIGHT = 200

# Button Functions

def addItem():

    def addToDB():
        pass
        # TODO
        # Here is where the sql commands would go to add the item to the database
        # Commands would need to depend on radio button selection
        # Need to add error handling for if the user doesn't enter a value or value is already in db
        # ItemID(M### or B###) and MemberID(U###) should be auto generated and CheckOut Status should be false by default
     

    def renderAddItemWindow():

        for widget in renderFrame.winfo_children():
            widget.destroy()

        if selectedItem.get() == 1:

            nameLabel = tk.Label(renderFrame, text="Name:", fg="black", anchor="w")
            nameLabel.place(relx=0.05, rely=0, relwidth=1, relheight=0.1)

            nameEntry = tk.Entry(renderFrame)
            nameEntry.place(relx = 0.05, rely = 0.1, relwidth = 0.8, relheight = 0.15)

        if selectedItem.get() == 2:

            titleLabel = tk.Label(renderFrame, text="Title:", fg="black", anchor="w")
            titleLabel.place(relx=0.05, rely=0, relwidth=1, relheight=0.1)

            titleEntry = tk.Entry(renderFrame)
            titleEntry.place(relx = 0.05, rely = 0.1, relwidth = 0.8, relheight = 0.15)

            authorLabel = tk.Label(renderFrame, text="Author:", fg="black", anchor="w")
            authorLabel.place(relx=0.05, rely=0.25, relwidth=1, relheight=0.1)

            authorEntry = tk.Entry(renderFrame)
            authorEntry.place(relx = 0.05, rely = 0.35, relwidth = 0.8, relheight = 0.15)

        if selectedItem.get() == 3:

            titleLabel = tk.Label(renderFrame, text="Title:", fg="black", anchor="w")
            titleLabel.place(relx=0.05, rely=0, relwidth=1, relheight=0.1)

            titleEntry = tk.Entry(renderFrame)
            titleEntry.place(relx = 0.05, rely = 0.1, relwidth = 0.8, relheight = 0.15)

            directorLabel = tk.Label(renderFrame, text="Director:", fg="black", anchor="w")
            directorLabel.place(relx=0.05, rely=0.25, relwidth=1, relheight=0.1)

            directorEntry = tk.Entry(renderFrame)
            directorEntry.place(relx = 0.05, rely = 0.35, relwidth = 0.8, relheight = 0.15)

        addButton = tk.Button(renderFrame, text="Add", fg="black", command=addToDB, anchor="center")
        addButton.place(relx=0.4, rely=0.75, relwidth=0.2, relheight=0.2)


    addItemWindow = tk.Toplevel(root)
    addItemWindow.title("Add Item")
    addItemWindow.resizable(False, False)
    addItemWindow.grab_set()
    x = (screenWidth/2) - (NEW_WINDOW_WIDTH/2)
    y = (screenHeight/2) - (NEW_WINDOW_HEIGHT/2)
    addItemWindow.geometry('%dx%d+%d+%d' % (NEW_WINDOW_WIDTH, NEW_WINDOW_HEIGHT, x, y))
    selectedItem = tk.IntVar()

    radioButtonFrame = tk.Frame(addItemWindow)
    radioButtonFrame.place(relx=0, rely=0, anchor="nw", relwidth=1, relheight=0.2)

    renderFrame = tk.Frame(addItemWindow)
    renderFrame.place(relx=0, rely=0.2, anchor="nw", relwidth=1, relheight=0.8)

    memberRB = tk.Radiobutton(radioButtonFrame, text="Member", variable=selectedItem, value=1, command=renderAddItemWindow)
    memberRB.grid(row=0, column=0)

    bookRB = tk.Radiobutton(radioButtonFrame, text="Book", variable=selectedItem, value=2, command=renderAddItemWindow)
    bookRB.grid(row=0, column=1)

    movieRB = tk.Radiobutton(radioButtonFrame, text="Movie", variable=selectedItem, value=3, command=renderAddItemWindow)
    movieRB.grid(row=0, column=2)



    


# Add Item Button
addItemButton = tk.Button(root, text="Add Item", command=addItem)
addItemButton.place(relx = 0.05, rely = 0.05, relwidth=BUTTON_REL_WIDTH, relheight=BUTTON_REL_HEIGHT)

# Delete Item Button
deleteRowButton = tk.Button(root, text="Delete Item")
deleteRowButton.place(relx = 0.05, rely = 0.15, relwidth=BUTTON_REL_WIDTH, relheight=BUTTON_REL_HEIGHT)

# Checkout Item Button
checkoutItemButton = tk.Button(root, text="Checkout Item")
checkoutItemButton.place(relx = 0.05, rely = 0.25, relwidth=BUTTON_REL_WIDTH, relheight=BUTTON_REL_HEIGHT)

# Return Item Button
returnItemButton = tk.Button(root, text="Return Item")
returnItemButton.place(relx = 0.05, rely = 0.35, relwidth=BUTTON_REL_WIDTH, relheight=BUTTON_REL_HEIGHT)

#TODO 
# Buttons for searching for items
# Buttons for other pre-defined queries

# A frame that will display tables and search results




root.mainloop()
