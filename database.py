import sqlite3
import tkinter as tk


# code for creating table student
# conn = sqlite3.connect("examhall.db")
# c = conn.cursor()
# c.execute("DROP TABLE IF EXISTS stud")
# conn.commit()
# conn.close()


# conn = sqlite3.connect("examhall.db")
# c = conn.cursor()
# c.execute(
#     """CREATE TABLE stud(
#                 username text primary key,
#                 password text,
#                 name text,
#                 department text,
#                 sem text,
#                 hall text
#          )"""
# )
# conn.commit()
# conn.close()


# code for creating table teacher
# c=conn.cursor()
# c.execute("""CREATE TABLE teacher(
# teachername text,
# password text
# )""")
# conn.commit()
# conn.close()


# function for adding users
def add_student(list):
    try:
        conn = sqlite3.connect("examhall.db")
        c = conn.cursor()
        u, p, n, s, d, b = list
        c.execute(f"INSERT INTO stud VALUES('{u}','{p}','{n}','{s}','{d}','{b}')")
    except Exception as e:
        print(e)
        return False
    finally:
        conn.commit()
        conn.close()
    return True


# classes = [
#     "adr20cs",
#     "adr20ec",
#     "adr20ee",
#     "adr20me",
#     "adr21cs",
#     "adr21ec",
#     "adr21ee",
#     "adr21me",
# ]
# for cls in classes:
#     for i in range(1, 61):
#         uname = f"{cls}{i:03}"
#         pas = f"pass{cls}{i:03}"
#         name = f"name{cls}{i}"
#         data = (uname, pas, name, "S6", cls[5:7], "")
#         add_student(data)


# function for adding teachers
def add_teacher(list):
    try:
        conn = sqlite3.connect("examhall.db")
        c = conn.cursor()
        c.executemany("INSERT INTO teacher VALUES(?,?)", (list))
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
    finally:
        conn.commit()
        conn.close()


# items=[
# ('shibu','shibu@123'),
# ('honey','honey@123),
# ('girija','girija@123'),
# ('sreedeepa','sdp@123'),
# ('jayaram','jk@123'),
# ('manju','manju@123'),
# ('keerthana','keerthana@123'),
# ('jyothi','jyothi@123'),
# ('reshma','reshma@123'),
# ]
# add_teacher(items)


# Function to check if the username and password of students match in the database
def check_credentials(username, password):
    conn = sqlite3.connect("examhall.db")
    c = conn.cursor()

    # Using a parameterized query to avoid SQL injection
    c.execute(
        "SELECT * FROM stud WHERE username = ? AND password = ?", (username, password)
    )

    # Fetch the first matching row
    result = c.fetchone()

    conn.close()

    # If a row is fetched, the username and password match
    if result:
        return True
    else:
        return False


# Function to check if the username and password  of teachers match in the database
def check_teacher_credentials(teachername, password):
    conn = sqlite3.connect("examhall.db")
    c = conn.cursor()

    # Using a parameterized query to avoid SQL injection
    c.execute(
        "SELECT * FROM teacher WHERE teachername = ? AND password = ?",
        (teachername, password),
    )

    # Fetch the first matching row
    result = c.fetchone()

    conn.close()

    # If a row is fetched, the username and password match
    if result:
        return True
    else:
        return False


# c=conn.cursor()
# c.execute("ALTER TABLE stud ADD COLUMN name text")
# c.execute("ALTER TABLE stud ADD COLUMN dept text")
# c.execute("ALTER TABLE stud ADD COLUMN sem text")
# c.execute("ALTER TABLE stud ADD COLUMN bench text")
# conn.commit()
# conn.close()


def search(username):
    # Connect to the Database
    conn = sqlite3.connect("examhall.db")
    c = conn.cursor()

    # Search for the user in the 'user' table
    c.execute(
        "SELECT username,name,department,sem,hall FROM stud WHERE username = ?",
        (username,),
    )

    # Fetch the first matching row
    result = c.fetchone()

    # Commit and Close the Connection
    conn.commit()
    conn.close()

    return result


def delete_user(username):
    # Connect to the Database
    try:
        conn = sqlite3.connect("examhall.db")
        c = conn.cursor()
        # Delete the row from the 'stud' table based on the username (USN)
        c.execute(f"DELETE FROM stud WHERE username = '{username}'")
    except Exception as e:
        # If an error occurs during deletion, print the error for debugging purposes
        print(f"Error deleting user: {e}")
        return False
    finally:
        conn.commit()
        conn.close()
    return True


# def add_student(list):
#     try:
#         conn = sqlite3.connect("examhall.db")
#         c = conn.cursor()
#         u, p, n, s, d, b = list
#         c.execute(f"INSERT INTO stud VALUES('{u}','{p}','{n}','{s}','{d}','{b}')")
#         conn.commit()
#         conn.close()
#         return True
#     except Exception as e:
#         print(f"Error registering a user: {e}")
#         return False


def update_student(student_data):
    try:
        conn = sqlite3.connect("examhall.db")
        c = conn.cursor()

        sid, name, dept, sem, bench = student_data

        # Using a parameterized query to avoid SQL injection
        c.execute(
            "UPDATE stud SET name=?, department=?, sem=? WHERE username=?",
            (name, dept, sem, sid),
        )
    except Exception as e:
        print(e)
    finally:
        conn.commit()
        conn.close()
