from tkinter import ttk
from tkinter import *

window = Tk()
window.title("LIBRARY MANAGEMENT SYSTEM")
window.geometry("950x850")
window.config(background="white")

try:
    notebook = ttk.Notebook(window)
    tab_1 = Frame(notebook)
    tab_2 = Frame(notebook)
    notebook.add(tab_1, text="Tab 1")
    notebook.add(tab_2, text="Tab 2")
    notebook.pack(expand=True, fill="both")

    # placing tab 1
    search_term = Entry(tab_1, font=("arial", 15), fg="white", bg="black", width=45)
    search_term.pack(side=LEFT)
    search_btn = Button(
        tab_1,
        text="Search in tab 1",
        font=("arial", 15),
        command=True,
    )
    search_btn.pack(side=LEFT)

    # placing tab 1
    search_term = Entry(tab_2, font=("arial", 15), fg="white", bg="black", width=45)
    search_term.pack(side=LEFT)
    search_btn = Button(
        tab_2,
        text="Search in tab 2",
        font=("arial", 15),
        command=True,
    )
    search_btn.pack(side=LEFT)
    
    

    window.mainloop()

except Exception as e:
    print(e)
