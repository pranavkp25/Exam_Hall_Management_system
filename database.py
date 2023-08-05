import sqlite3

conn = sqlite3.connect('examhall.db')

#code for creating table student
#c=conn.cursor()
#c.execute("""CREATE TABLE stud(
         #  username text, 
         # password text
         # )""")
#conn.commit()
#conn.close()


#code for creating table teacher
#c=conn.cursor()
#c.execute("""CREATE TABLE teacher(
          #teachername text, 
         # password text
         # )""")
#conn.commit()
#conn.close()

#function for adding users
def add_student(list):
  conn = sqlite3.connect('examhall.db')
  c = conn.cursor()
  c.executemany("INSERT INTO stud VALUES(?,?,?,?,?,?)",(list))
  conn.commit()
  conn.close()


#function for adding teachers
def add_teacher(list):
  conn = sqlite3.connect('examhall.db')
  c = conn.cursor()
  c.executemany("INSERT INTO teacher VALUES(?,?)",(list))
  conn.commit()
  conn.close()


#items=[
    #('shibu','shibu@123'),
    #('honey','honey@123),
   # ('girija','girija@123'),
    #('sreedeepa','sdp@123'),
    #('jayaram','jk@123'),
    #('manju','manju@123'),
    #('keerthana','keerthana@123'),
    #('jyothi','jyothi@123'),
    #('reshma','reshma@123'),
    #]
#add_teacher(items)


 # Function to check if the username and password of students match in the database
def check_credentials(username, password):
    conn = sqlite3.connect('examhall.db')
    c = conn.cursor()

    # Using a parameterized query to avoid SQL injection
    c.execute("SELECT * FROM stud WHERE username = ? AND password = ?", (username, password))
    
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
    conn = sqlite3.connect('examhall.db')
    c = conn.cursor()

    # Using a parameterized query to avoid SQL injection
    c.execute("SELECT * FROM teacher WHERE teachername = ? AND password = ?", (teachername, password))
    
    # Fetch the first matching row
    result = c.fetchone()

    conn.close()

    # If a row is fetched, the username and password match
    if result:
        return True
    else:
        return False
    

#c=conn.cursor()
#c.execute("ALTER TABLE stud ADD COLUMN name text")
#c.execute("ALTER TABLE stud ADD COLUMN dept text")
#c.execute("ALTER TABLE stud ADD COLUMN sem text")
#c.execute("ALTER TABLE stud ADD COLUMN bench text")
#conn.commit()
#conn.close()


def search(username):
    # Connect to the Database
    conn = sqlite3.connect('examhall.db')
    c = conn.cursor()

    # Search for the user in the 'user' table
    c.execute("SELECT username,name,dept,sem,bench FROM stud WHERE username = ?", (username,))
    
    # Fetch the first matching row
    result = c.fetchall()

    # Commit and Close the Connection
    conn.commit()
    conn.close()

    return result


def delete_user(username):
    # Connect to the Database
    conn = sqlite3.connect('examhall.db')
    c = conn.cursor()

    try:
        # Delete the row from the 'stud' table based on the username (USN)
        c.execute("DELETE FROM stud WHERE username = ?", (username,))

        # Commit and Close the Connection
        conn.commit()
        conn.close()

        return True  # Return True to indicate success
    except Exception as e:
        # If an error occurs during deletion, print the error for debugging purposes
        print(f"Error deleting user: {e}")

    # If the function hasn't returned True yet, it means deletion was unsuccessful
    return False



def add_student(list):
    conn = sqlite3.connect('examhall.db')
    c = conn.cursor()
    c.executemany("INSERT INTO stud VALUES(?,?,?,?,?,?)", list)
    conn.commit()
    conn.close()

def update_student(student_data):
    conn = sqlite3.connect('examhall.db')
    c = conn.cursor()
    
    sid, name, dept, sem, bench = student_data 

    # Using a parameterized query to avoid SQL injection
    c.execute("UPDATE stud SET name=?, dept=?, sem=?, bench=? WHERE username=?",
              (name, dept, sem, bench, sid))

    conn.commit()
    conn.close()


