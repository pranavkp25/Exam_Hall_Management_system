from tkinter import *
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
from database import *
from seating import *


def login():
    username = username_entry_tab1.get()
    password = password_entry_tab1.get()

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
    search_button_reg.config(state=tk.NORMAL)
    view_allotment_button.config(state=tk.NORMAL)
    search_button.config(state=tk.NORMAL)


# Function to enable features for the student role
def enable_student_features():
    register_button.config(state=tk.DISABLED)
    edit_button.config(state=tk.DISABLED)
    delete_button.config(state=tk.DISABLED)
    search_button_reg.config(state=tk.DISABLED)
    view_allotment_button.config(state=tk.DISABLED)
    search_button.config(state=tk.NORMAL)


# Function to enable default features
def enable_default_features():
    register_button.config(state=tk.DISABLED)
    edit_button.config(state=tk.DISABLED)
    delete_button.config(state=tk.DISABLED)
    search_button.config(state=tk.DISABLED)
    search_button_reg.config(state=tk.DISABLED)
    view_allotment_button.config(state=tk.DISABLED)


# Function to handle the registration of a new student
def register_student():
    usn = usn_entry.get()
    pswd = pswd_entry.get()
    name = name_entry.get()
    dept = department_entry.get()
    sem = sem_entry.get()
    hall =""

    if usn and name and dept and sem and pswd:
        # Prepare the data to insert into the database
        student_data = (usn, pswd, name, dept, sem, hall)

        # Add the student to the database
        if add_student(student_data):
            messagebox.showinfo("Success", "Student registered successfully.")
            clear_entries()
        else:
            messagebox.showwarning("Warning", "Failed to register a user")

    else:
        messagebox.showwarning("Warning", "Please fill in all the fields.")


# Function to handle the search and display of student records
def search_students(entry, tv):
    search_query = entry.get()
    print(search_query)

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
        item = tv_tab3.item(tv_tab3.focus())
        usn = item["values"][0]
        name = name_entry.get()
        department = department_entry.get()
        sem = sem_entry.get()
        hall = item["values"][4]
        name_entry.delete(0, END)
        department_entry.delete(0, END)
        sem_entry.delete(0, END)

        if usn and name and department and sem:
            # Prepare the data to update in the database
            student_data = (usn, name, department, sem, hall)

            # Update the student's data in the database
            update_student(student_data)
            print_table(student_data, tv_tab3)

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
        item = tv_tab3.item(tv_tab3.focus())
        username = item["values"][0]
        name_entry.delete(0, END)
        department_entry.delete(0, END)
        sem_entry.delete(0, END)

        if username:
            # Delete the student from the database using the delete_user function
            if delete_user(username):
                tv_tab3.delete(*tv_tab3.get_children())
                messagebox.showinfo("Success", "Student deleted successfully.")
            else:
                messagebox.showwarning(
                    "Warning",
                    "Failed to delete student. Please check the username (USN).",
                )
        else:
            messagebox.showwarning(
                "Warning", "Please enter a username (USN) to delete."
            )
    except Exception as e:
        messagebox.showerror("Error", "An error occurred while deleting the student.")


# Function to clear the entry fields
def clear_entries():
    usn_entry.delete(0, tk.END)
    pswd_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    department_entry.delete(0, tk.END)
    sem_entry.delete(0, tk.END)
    # bench_entry.delete(0, tk.END)


def clear_entries_1():
    username_entry_tab1.delete(0, tk.END)
    password_entry_tab1.delete(0, tk.END)


# tv functions
def print_table(data, tv):
    tv.delete(*tv.get_children())
    tv.insert("", "end", values=data)


def tv_focus_fun(e):
    try:
        if edit_button.cget("state") == tk.DISABLED:
            return
        item = tv_tab3.item(tv_tab3.focus())
        name_entry.delete(0, END)
        name_entry.insert(0, item["values"][1])
        department_entry.delete(0, END)
        department_entry.insert(0, item["values"][2])
        sem_entry.delete(0, END)
        sem_entry.insert(0, item["values"][3])
        # bench_entry.delete(0, END)
        # bench_entry.insert(0, item["values"][4])
    except Exception as e:
        print(e)


def move_widget():
    x = moving_widget.winfo_x()
    new_x = x + 3  # Update the x-coordinate
    moving_widget.place(
        x=new_x, y=root.winfo_height() - widget_height
    )  # Keep y-coordinate at the bottom
    root.after(50, move_widget)  # Call move_widget again after 50ms


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

# Create a notebook widget to hold different tabs
notebook = ttk.Notebook(root)
tab_1 = Frame(notebook)
tab_2 = Frame(notebook)
tab_3 = Frame(notebook)
tab_4 = Frame(notebook)
tab_5 = Frame(notebook)
notebook.add(tab_1, text="login")
notebook.add(tab_2, text="search")
notebook.add(tab_3, text="Student Registration")
notebook.add(tab_4, text="Seating Arrangement")
notebook.add(tab_5, text="View Allocation")
notebook.pack(expand=True, fill="both")


# Create and place widgets for login
login_frame_tab1 = tk.LabelFrame(
    tab_1,
    text="Login",
    padx=8,
    pady=8,
    bg="#CCCCCC",
    fg="#080202",
    font=("Times New Roman", 14),
)
login_frame_tab1.pack(pady=8)

username_label_tab1 = tk.Label(
    login_frame_tab1,
    text="Username:",
    bg="#CCCCCC",
    fg="#080202",
    font=("Times New Roman", 14),
)
username_label_tab1.grid(row=0, column=0, sticky=tk.E)
username_entry_tab1 = tk.Entry(login_frame_tab1, font=("Times New Roman", 14))
username_entry_tab1.grid(row=0, column=1)

password_label_tab1 = tk.Label(
    login_frame_tab1,
    text="Password:",
    bg="#CCCCCC",
    fg="#080202",
    font=("Times New Roman", 14),
)
password_label_tab1.grid(row=1, column=0, sticky=tk.E)
password_entry_tab1 = tk.Entry(login_frame_tab1, show="*", font=("Times New Roman", 14))
password_entry_tab1.grid(row=1, column=1)

login_button_tab1 = tk.Button(
    login_frame_tab1,
    text="Login",
    command=login,
    bg="#CCCCCC",
    fg="#080202",
    font=("Times New Roman", 14),
)
login_button_tab1.grid(row=2, column=1, pady=8)


# Create and place widgets for student registration
registration_frame = tk.LabelFrame(
    tab_3,
    text="Student Registration",
    padx=8,
    pady=8,
    bg="#CCCCCC",
    fg="#080202",
    font=("Times New Roman", 14),
)
registration_frame.pack(pady=8)

usn_label = tk.Label(
    registration_frame,
    text="USN:",
    bg="#CCCCCC",
    fg="#080202",
    font=("Times New Roman", 14),
)
usn_label.grid(row=0, column=0, sticky=tk.E)
usn_entry = tk.Entry(registration_frame, font=("Times New Roman", 14))
usn_entry.grid(row=0, column=1)

pswd_label = tk.Label(
    registration_frame,
    text="Pswd:",
    bg="#CCCCCC",
    fg="#080202",
    font=("Times New Roman", 14),
)
pswd_entry = tk.Entry(registration_frame, show="*", font=("Times New Roman", 14))
pswd_label.grid(row=1, column=0, sticky=tk.E)
pswd_entry.grid(row=1, column=1)

name_label = tk.Label(
    registration_frame,
    text="Name:",
    bg="#CCCCCC",
    fg="#080202",
    font=("Times New Roman", 14),
)
name_label.grid(row=2, column=0, sticky=tk.E)
name_entry = tk.Entry(registration_frame, font=("Times New Roman", 14))
name_entry.grid(row=2, column=1)

department_label = tk.Label(
    registration_frame,
    text="Department:",
    bg="#CCCCCC",
    fg="#080202",
    font=("Times New Roman", 14),
)
department_label.grid(row=3, column=0, sticky=tk.E)
department_entry = tk.Entry(registration_frame, font=("Times New Roman", 14))
department_entry.grid(row=3, column=1)

sem_label = tk.Label(
    registration_frame,
    text="Sem:",
    bg="#CCCCCC",
    fg="#080202",
    font=("Times New Roman", 14),
)
sem_label.grid(row=4, column=0, sticky=tk.E)
sem_entry = tk.Entry(registration_frame, font=("Times New Roman", 14))
sem_entry.grid(row=4, column=1)

# bench_label = tk.Label(
# registration_frame,
# text="Bench:",
# bg="#CCCCCC",
# fg="#080202",
# font=("Times New Roman", 14),
# )
# bench_label.grid(row=5, column=0, sticky=tk.E)
# bench_entry = tk.Entry(registration_frame, font=("Times New Roman", 14))
# bench_entry.grid(row=5, column=1)

register_button = tk.Button(
    registration_frame,
    text="Register",
    command=register_student,
    bg="#CCCCCC",
    fg="#080202",
    font=("Times New Roman", 14),
)
register_button.grid(row=6, column=1, pady=8)
register_button.config(state=tk.DISABLED)

# Set registration frame background color
registration_frame.configure(bg="#CCCCCC")

# Create and place widgets for search and display for search tab
search_frame = tk.LabelFrame(
    tab_2,
    text="Search",
    padx=8,
    pady=8,
    bg="#CCCCCC",
    fg="#080202",
    font=("Times New Roman", 14),
)
search_frame.pack(pady=8)

search_label = tk.Label(
    search_frame,
    text="Search by USN :",
    bg="#CCCCCC",
    fg="#080202",
    font=("Times New Roman", 14),
)
search_label.grid(row=0, column=0, sticky=tk.E)
search_entry_tab2 = tk.Entry(search_frame, font=("Times New Roman", 14))
search_entry_tab2.grid(row=0, column=1)

search_button = tk.Button(
    search_frame,
    text="Search",
    command=lambda: search_students(search_entry_tab2, tv_tab2),
    bg="#CCCCCC",
    fg="#080202",
    font=("Times New Roman", 14),
)
search_button.grid(row=0, column=2, padx=8)
search_button.config(state=tk.DISABLED)

# Create and place widgets for search and display for registration tab
search_frame = tk.LabelFrame(
    tab_3,
    text="Search",
    padx=8,
    pady=8,
    bg="#CCCCCC",
    fg="#080202",
    font=("Times New Roman", 14),
)
search_frame.pack(pady=8)

search_label = tk.Label(
    search_frame,
    text="Search by USN :",
    bg="#CCCCCC",
    fg="#080202",
    font=("Times New Roman", 14),
)
search_label.grid(row=0, column=0, sticky=tk.E)
search_entry_tab3 = tk.Entry(search_frame, font=("Times New Roman", 14))
search_entry_tab3.grid(row=0, column=1)

search_button_reg = tk.Button(
    search_frame,
    text="Search",
    command=lambda: search_students(search_entry_tab3, tv_tab3),
    bg="#CCCCCC",
    fg="#080202",
    font=("Times New Roman", 14),
)
search_button_reg.grid(row=0, column=2, padx=8)
search_button_reg.config(state=tk.DISABLED)

# table view for search tab
tv_frame_tab2 = tk.LabelFrame(
    tab_2,
    text="Search Result",
    padx=10,
    pady=10,
    bg="#CCCCCC",
    fg="#080202",
    font=("Times New Roman", 14),
)
tv_frame_tab2.pack(pady=8)
tv_tab2 = ttk.Treeview(
    tv_frame_tab2, columns=(1, 2, 3, 4, 5), show="headings", height=5
)
tv_tab2.pack(pady=2, fill="both", padx=2)
tv_tab2.heading(1, text="USERNAME")
tv_tab2.column(1, width=150)
tv_tab2.heading(2, text="NAME")
tv_tab2.column(2, width=150)
tv_tab2.heading(3, text="DEPT")
tv_tab2.column(3, width=100)
tv_tab2.heading(4, text="SEM")
tv_tab2.column(4, width=100)
tv_tab2.heading(5, text="HALL")
tv_tab2.column(5, width=100)
tv_tab2.bind("<Double 1>", tv_focus_fun)

# table view for registration tab
tv_frame_tab3 = tk.LabelFrame(
    tab_3,
    text="Search Result",
    padx=10,
    pady=10,
    bg="#CCCCCC",
    fg="#080202",
    font=("Times New Roman", 14),
)
tv_frame_tab3.pack(pady=8)
tv_tab3 = ttk.Treeview(
    tv_frame_tab3, columns=(1, 2, 3, 4, 5), show="headings", height=5
)
tv_tab3.pack(pady=2, fill="both", padx=2)
tv_tab3.heading(1, text="USERNAME")
tv_tab3.column(1, width=150)
tv_tab3.heading(2, text="NAME")
tv_tab3.column(2, width=150)
tv_tab3.heading(3, text="DEPT")
tv_tab3.column(3, width=100)
tv_tab3.heading(4, text="SEM")
tv_tab3.column(4, width=100)
tv_tab3.heading(5, text="HALL")
tv_tab3.column(5, width=100)
tv_tab3.bind("<Double 1>", tv_focus_fun)


# Create and place buttons for edit and delete
edit_button = tk.Button(
    tab_3,
    text="Update",
    command=edit_student,
    bg="#CCCCCC",
    fg="#080202",
    font=("Times New Roman", 14),
)
edit_button.pack(pady=8)
edit_button.config(state=tk.DISABLED)

delete_button = tk.Button(
    tab_3,
    text="Delete",
    command=delete_student,
    bg="#CCCCCC",
    fg="#080202",
    font=("Times New Roman", 14),
)
delete_button.pack(pady=8)
delete_button.config(state=tk.DISABLED)


# Create and place widgets for seating arrangement
seating_frame = tk.LabelFrame(
    tab_4,
    text="Seating Arrangement",
    padx=8,
    pady=8,
    bg="#CCCCCC",
    fg="#080202",
    font=("Times New Roman", 14),
)
seating_frame.pack(pady=8)

no_of_cls_label = tk.Label(
    seating_frame,
    text="Number of Classes:",
    bg="#CCCCCC",
    fg="#080202",
    font=("Times New Roman", 14),
)
no_of_cls_label.grid(row=0, column=0, sticky=tk.E)
no_of_cls_entry = tk.Entry(seating_frame, font=("Times New Roman", 14))
no_of_cls_entry.grid(row=0, column=1, columnspan=5)


class_dmns_label = tk.Label(
    seating_frame,
    text="Exam Hall Dimensions :",
    bg="#CCCCCC",
    fg="#080202",
    font=("Times New Roman", 14),
)
class_dmns_label.grid(row=3, column=0, sticky=tk.E)
class_dmns_entry = tk.Entry(seating_frame, font=("Times New Roman", 14))
class_dmns_entry.grid(row=3, column=1)

cls_details_view = False
cls_details_list = []


def cls_detail_submit_btn_fun():
    try:
        students = []
        noOfSubjects = int(no_of_cls_entry.get())
        row, col = (int(x) for x in class_dmns_entry.get().split("x"))
        for cls_details in cls_details_list:
            if (
                cls_details[0].get() == ""
                or cls_details[1].get() == ""
                or cls_details[2].get() == ""
            ):
                messagebox.showwarning("Warning", "Please fill in all the fields.")
                return
            adr, frm, to = (
                cls_details[0].get(),
                int(cls_details[1].get()),
                int(cls_details[2].get()),
            )
            students.append([adr, int(to) - int(frm) + 1, int(frm)])

        students.sort(key=lambda x: x[1], reverse=True)
    except:
        messagebox.showwarning("Warning", "Invalid Entry !")

    try:
        data = "\n"
        count = 1
        seated_halls = setSeating(students, row, col)
        for hall in seated_halls:
            hallno = "hall-" + str(count)
            data = data + hallno + "\n"
            for hrow in hall:
                data = data + "\t"
                for elm in hrow:
                    data = data + elm + "\t"
                    conn = sqlite3.connect("examhall.db")
                    c = conn.cursor()
                    c.execute(f"update stud set hall='{hallno}' where username='{elm}'")
                    conn.commit()
                    conn.close()
                data = data + "\n"
            data = data + "\n\n"
            count += 1

        allocation_frame = tk.LabelFrame(
            tab_5,
            text="Seating Allocation View",
            padx=8,
            pady=8,
            bg="#CCCCCC",
            fg="#080202",
            font=("Times New Roman", 14),
        )
        allocation_frame.pack(pady=8)
        text_label = tk.Label(allocation_frame, text=data)
        text_label.pack()

        with open("allocation.txt", "w") as file:
            file.write(data)

    except Exception as e:
        print(e)


def list_class_details_entry(r):
    global cls_details_view
    if cls_details_view:
        return
    list_class_details_entry_frame = tk.LabelFrame(
        tab_4,
        text="Seating Arrangement",
        padx=8,
        pady=8,
        bg="#CCCCCC",
        fg="#080202",
        font=("Times New Roman", 14),
    )
    list_class_details_entry_frame.pack(pady=8)
    for i in range(r):
        cls_details = []
        # adr
        cls_adr_label = tk.Label(
            list_class_details_entry_frame,
            text="adr: ",
            bg="#CCCCCC",
            fg="#080202",
            font=("Times New Roman", 14),
        )
        cls_adr_label.grid(row=5 + i, column=0, sticky=tk.E)
        cls_adr_entry = tk.Entry(
            list_class_details_entry_frame, font=("Times New Roman", 14)
        )
        cls_adr_entry.grid(row=5 + i, column=1)
        cls_details.append(cls_adr_entry)
        # from
        cls_from_label = tk.Label(
            list_class_details_entry_frame,
            text="from: ",
            bg="#CCCCCC",
            fg="#080202",
            font=("Times New Roman", 14),
        )
        cls_from_label.grid(row=5 + i, column=2, sticky=tk.E)
        cls_from_entry = tk.Entry(
            list_class_details_entry_frame, font=("Times New Roman", 14)
        )
        cls_from_entry.grid(row=5 + i, column=3)
        cls_details.append(cls_from_entry)
        # to
        cls_to_label = tk.Label(
            list_class_details_entry_frame,
            text="to: ",
            bg="#CCCCCC",
            fg="#080202",
            font=("Times New Roman", 14),
        )
        cls_to_label.grid(row=5 + i, column=4, sticky=tk.E)
        cls_to_entry = tk.Entry(
            list_class_details_entry_frame, font=("Times New Roman", 14)
        )
        cls_to_entry.grid(row=5 + i, column=5)
        cls_details.append(cls_to_entry)
        cls_details_view = True
        cls_details_list.append(cls_details)
    Submit_btn_tab4 = tk.Button(
        tab_4,
        text="Submit",
        command=cls_detail_submit_btn_fun,
        bg="#CCCCCC",
        fg="#080202",
        font=("Times New Roman", 14),
    )
    Submit_btn_tab4.pack()


view_allotment_button = tk.Button(
    seating_frame,
    text="Enter",
    command=lambda: list_class_details_entry(int(no_of_cls_entry.get())),
    bg="#CCCCCC",
    fg="#080202",
    font=("Times New Roman", 14),
)
view_allotment_button.grid(row=4, column=0)
view_allotment_button.config(state=tk.DISABLED)

# moving widget
widget_width = 50
widget_height = 50

moving_widget = tk.Label(
    root,
    text="Exam Hall Management System",
    bg="lightblue",
    font=("Times New Roman", 20, "bold"),
)
moving_widget.place(
    x=50, y=root.winfo_height() - widget_height
)  # Initial position at the bottom

move_widget()

# Run the main event loop
root.mainloop()
