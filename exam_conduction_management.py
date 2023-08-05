from tkinter import *
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
from database import*
from seating import*

def login():
    username = username_entry.get()
    password = password_entry.get()
    
    if username == "" or password == "":
        messagebox.showerror("Login Failed", "Please enter a username and password.")
        return
    
    if check_teacher_credentials(username, password):
        # teacher login
        messagebox.showinfo("Login Successful", "Welcome " + username)
        enable_admin_features()
        clear_entries_1()

    elif check_credentials(username, password):
        # Student login
        messagebox.showinfo("Login Successful", "Welcome " + username)
        enable_student_features()
        clear_entries_1()
        
    else:
        # Invalid credentials
        messagebox.showerror("Login Failed", "Invalid username or password.")
        enable_default_features()
        clear_entries_1()


# Function to enable features for the admin role
def enable_admin_features():
    register_button.config(state=tk.NORMAL)
    edit_button.config(state=tk.NORMAL)
    delete_button.config(state=tk.NORMAL)
    search_button.config(state=tk.NORMAL)

# Function to enable features for the student role
def enable_student_features():
    register_button.config(state=tk.DISABLED)
    edit_button.config(state=tk.DISABLED)
    delete_button.config(state=tk.DISABLED)
    search_button.config(state=tk.NORMAL)

# Function to enable default features
def enable_default_features():
    register_button.config(state=tk.DISABLED)
    edit_button.config(state=tk.DISABLED)
    delete_button.config(state=tk.DISABLED)
    search_button.config(state=tk.DISABLED)

# Function to handle the registration of a new student
def register_student():
    usn = usn_entry.get()
    pswd =pswd_entry.get()
    name = name_entry.get()
    dept = department_entry.get()
    sem = sem_entry.get()
    bench = bench_entry.get()

    if usn and name and dept and sem and bench:
        # Prepare the data to insert into the database
        student_data = (usn, pswd,name, dept, sem, bench)

        # Add the student to the database
        add_student([student_data])
        
        messagebox.showinfo("Success", "Student registered successfully.")
        clear_entries()
    else:
        messagebox.showwarning("Warning", "Please fill in all the fields.")

# Function to handle the search and display of student records
def search_students():
    search_query = search_entry.get()

    if search_query:
        try:
            result = search(search_query)

            if result:
                print_table(result, tv)
            else:
                # Display a message if no result is found
                messagebox.showinfo("Search Result", "No matching student found.")

        except Exception as e:
            messagebox.showwarning("Warning", "An error occurred while searching.")
            print(e)  # You can print the error for debugging purposes

    else:
        # Display a message if no search query is provided
        messagebox.showwarning("Warning", "Please enter a search query.")
        
# Function to handle the editing and updating of student records

def edit_student():
    try:
        item = tv.item(tv.focus())
        usn = item["values"][0]
        name = name_entry.get()
        department = department_entry.get()
        sem = sem_entry.get()
        bench = bench_entry.get()
        
        
        if usn and name and department and sem and bench:
            # Prepare the data to update in the database
            student_data = [(usn, name, department, sem, bench)]

            # Update the student's data in the database
            update_student(student_data[0])
            print_table(student_data, tv)

            messagebox.showinfo("Success", "Student information updated successfully.")
            clear_entries()
            enable_admin_features()
        else:
            messagebox.showwarning("Warning", "Please fill in all the fields.")

    except Exception as e:
        pass



# Function to handle the deletion of student records

def delete_student():
    
    try:
        item = tv.item(tv.focus())
        username = item["values"][0]

        if username:
            # Delete the student from the database using the delete_user function
            if delete_user(username):
                tv.delete(*tv.get_children())
                messagebox.showinfo("Success", "Student deleted successfully.")
            else:
                messagebox.showwarning("Warning", "Failed to delete student. Please check the username (USN).")
        else:
            messagebox.showwarning("Warning", "Please enter a username (USN) to delete.")
    except Exception as e:
        messagebox.showerror("Error", "An error occurred while deleting the student.")


# Function to clear the entry fields
def clear_entries():
    usn_entry.delete(0, tk.END)
    pswd_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    department_entry.delete(0, tk.END)
    sem_entry.delete(0, tk.END)
    bench_entry.delete(0, tk.END)

def clear_entries_1():
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    
    
# tv functions
def print_table(data, tv):
    tv.delete(*tv.get_children())
    
    for d in data:
        tv.insert("", "end", values=d)
        
def tv_focus_fun(e):
    try:
        if edit_button.cget("state") == tk.DISABLED:
            return
        item = tv.item(tv.focus())
        name_entry.delete(0, END)
        name_entry.insert(0, item["values"][1])
        department_entry.delete(0, END)
        department_entry.insert(0, item["values"][2])
        sem_entry.delete(0, END)
        sem_entry.insert(0, item["values"][3])
        bench_entry.delete(0, END)
        bench_entry.insert(0, item["values"][4])
    except Exception as e:
        print(e)
        

# Create the main window
root = tk.Tk()
root.title("Exam Conduction Management")

# Set window size and position
window_width = 600
window_height = 400

filename = PhotoImage(file="sce.png")
background_label = Label(root, image=filename)

background_label.place(x=0, y=0, relwidth=1, relheight=1)
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Create and place widgets for login
login_frame = tk.LabelFrame(root, text="Login", padx=8, pady=8, bg="#CCCCCC", fg="#080202",
                            font=("Times New Roman", 14))
login_frame.pack(pady=8)

username_label = tk.Label(login_frame, text="Username:", bg="#CCCCCC", fg="#080202",
                          font=("Times New Roman", 14))
username_label.grid(row=0, column=0, sticky=tk.E)
username_entry = tk.Entry(login_frame, font=("Times New Roman", 14))
username_entry.grid(row=0, column=1)

password_label = tk.Label(login_frame, text="Password:", bg="#CCCCCC", fg="#080202",
                          font=("Times New Roman", 14))
password_label.grid(row=1, column=0, sticky=tk.E)
password_entry = tk.Entry(login_frame, show="*", font=("Times New Roman", 14))
password_entry.grid(row=1, column=1)

login_button = tk.Button(login_frame, text="Login", command=login, bg="#CCCCCC", fg="#080202",
                         font=("Times New Roman", 14))
login_button.grid(row=2, column=1, pady=8)

# Create and place widgets for student registration
registration_frame = tk.LabelFrame(root, text="Student Registration", padx=8, pady=8, bg="#CCCCCC",
                                   fg="#080202", font=("Times New Roman", 14))
registration_frame.pack(pady=8)

usn_label = tk.Label(registration_frame, text="USN:", bg="#CCCCCC", fg="#080202",
                     font=("Times New Roman", 14))
usn_label.grid(row=0, column=0, sticky=tk.E)
usn_entry = tk.Entry(registration_frame, font=("Times New Roman", 14))
usn_entry.grid(row=0, column=1)

pswd_label = tk.Label(registration_frame, text="Pswd:", bg="#CCCCCC", fg="#080202",
                     font=("Times New Roman", 14))
pswd_label.grid(row=1, column=0, sticky=tk.E)
pswd_entry = tk.Entry(registration_frame,show="*", font=("Times New Roman", 14))
pswd_entry.grid(row=1, column=1)

name_label = tk.Label(registration_frame, text="Name:", bg="#CCCCCC", fg="#080202",
                      font=("Times New Roman", 14))
name_label.grid(row=2, column=0, sticky=tk.E)
name_entry = tk.Entry(registration_frame, font=("Times New Roman", 14))
name_entry.grid(row=2, column=1)

department_label = tk.Label(registration_frame, text="Department:", bg="#CCCCCC", fg="#080202",
                            font=("Times New Roman", 14))
department_label.grid(row=3, column=0, sticky=tk.E)
department_entry = tk.Entry(registration_frame, font=("Times New Roman", 14))
department_entry.grid(row=3, column=1)

sem_label = tk.Label(registration_frame, text="Sem:", bg="#CCCCCC", fg="#080202",
                     font=("Times New Roman", 14))
sem_label.grid(row=4, column=0, sticky=tk.E)
sem_entry = tk.Entry(registration_frame, font=("Times New Roman", 14))
sem_entry.grid(row=4, column=1)

bench_label = tk.Label(registration_frame, text="Bench:", bg="#CCCCCC", fg="#080202",
                       font=("Times New Roman", 14))
bench_label.grid(row=5, column=0, sticky=tk.E)
bench_entry = tk.Entry(registration_frame, font=("Times New Roman", 14))
bench_entry.grid(row=5, column=1)

register_button = tk.Button(registration_frame, text="Register", command=register_student,
                            bg="#CCCCCC", fg="#080202", font=("Times New Roman", 14))
register_button.grid(row=6, column=1, pady=8)
register_button.config(state=tk.DISABLED)

# Set registration frame background color
registration_frame.configure(bg="#CCCCCC")

# Create and place widgets for search and display
search_frame = tk.LabelFrame(root, text="Search", padx=8, pady=8, bg="#CCCCCC", fg="#080202",
                             font=("Times New Roman", 14))
search_frame.pack(pady=8)

search_label = tk.Label(search_frame, text="Search by USN :", bg="#CCCCCC", fg="#080202",
                        font=("Times New Roman", 14))
search_label.grid(row=0, column=0, sticky=tk.E)
search_entry = tk.Entry(search_frame, font=("Times New Roman", 14))
search_entry.grid(row=0, column=1)

search_button = tk.Button(search_frame, text="Search", command=search_students,
                          bg="#CCCCCC", fg="#080202", font=("Times New Roman", 14))
search_button.grid(row=0, column=2, padx=8)

# table view
tv_frame = tk.LabelFrame(root, text="Search Result", padx=10, pady=10, bg="#CCCCCC",
                            fg="#080202", font=("Times New Roman", 14))
tv_frame.pack(pady=8)
tv = ttk.Treeview(tv_frame, columns=(1, 2, 3, 4, 5), show="headings", height=5)
tv.pack(pady=2, fill="both", padx=2)
tv.heading(1, text="USERNAME")
tv.column(1, width=150)
tv.heading(2, text="NAME")
tv.column(2, width=150)
tv.heading(3, text="DEPT")
tv.column(3, width=100)
tv.heading(4, text="SEM")
tv.column(4, width=100)
tv.heading(5, text="BENCH")
tv.column(5, width=100)
tv.bind("<Double 1>", tv_focus_fun)


# Create and place buttons for edit and delete
edit_button = tk.Button(root, text="Update", command=edit_student, bg="#CCCCCC", fg="#080202",
                        font=("Times New Roman", 14))
edit_button.pack(pady=8)
edit_button.config(state=tk.DISABLED)

delete_button = tk.Button(root, text="Delete", command=delete_student, bg="#CCCCCC", fg="#080202",
                          font=("Times New Roman", 14))
delete_button.pack(pady=8)
delete_button.config(state=tk.DISABLED)

# Set text widget font size
# display_text.configure(font=("Times New Roman", 14))

# Run the main event loop
root.mainloop()
