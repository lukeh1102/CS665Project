import tkinter as tk



root = tk.Tk()
root.resizable(False, False)

# Center Window
screenWidth = root.winfo_screenwidth()
screenHeight = root.winfo_screenheight()
windowWidth = 500
windowHeight = 500
x = (screenWidth/2) - (windowWidth/2)
y = (screenHeight/2) - (windowHeight/2)
root.geometry('%dx%d+%d+%d' % (windowWidth, windowHeight, x, y))

root.mainloop()
