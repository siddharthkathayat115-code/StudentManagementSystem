from tkinter import *
from tkinter import messagebox
import sqlite3

# -------------------- DATABASE SETUP --------------------

def connect_db():
    conn = sqlite3.connect("student_records.db")
    c = conn.cursor()

    # Student Table
    c.execute("""
        CREATE TABLE IF NOT EXISTS student (
            first_name TEXT,
            last_name TEXT,
            address TEXT
        )
    """)

    # User Table (for login)
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT,
            password TEXT
        )
    """)

    # Default User (if not exists)
    c.execute("SELECT * FROM users WHERE username='admin'")
    if not c.fetchone():
        c.execute("INSERT INTO users VALUES (?, ?)", ("admin", "1234"))

    conn.commit()
    conn.close()


def get_connection():
    return sqlite3.connect("student_records.db")


connect_db()

# -------------------- LOGIN WINDOW --------------------

def login():
    username = user_entry.get()
    password = pass_entry.get()

    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    result = c.fetchone()
    conn.close()

    if result:
        messagebox.showinfo("Success", "Login Successful")
        login_window.destroy()
        open_main_window()
    else:
        messagebox.showerror("Error", "Invalid Username or Password")


login_window = Tk()
login_window.title("Login")
login_window.geometry("400x300")
login_window.configure(bg="#34495e")

Label(login_window, text="Login System",
      font=("Segoe UI", 14, "bold"),
      bg="#34495e", fg="white").pack(pady=20)

Label(login_window, text="Username",
      bg="#34495e", fg="white").pack()

user_entry = Entry(login_window, width=30)
user_entry.pack(pady=5)

Label(login_window, text="Password",
      bg="#34495e", fg="white").pack()

pass_entry = Entry(login_window, width=30, show="*")
pass_entry.pack(pady=5)

Button(login_window, text="Login",
       width=20, bg="#1abc9c",
       command=login).pack(pady=20)

# -------------------- MAIN CRUD WINDOW --------------------

def open_main_window():

    def validate_fields():
        if f_name.get() == "" or l_name.get() == "" or address.get() == "":
            messagebox.showerror("Error", "All fields are required")
            return False
        return True

    def add_student():
        if not validate_fields():
            return

        conn = get_connection()
        c = conn.cursor()
        c.execute("INSERT INTO student VALUES (?,?,?)",
                  (f_name.get(), l_name.get(), address.get()))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Student Added")
        clear_fields()
        show_records()

    def show_records():
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT rowid, * FROM student")
        records = c.fetchall()
        conn.close()

        output.config(state=NORMAL)
        output.delete("1.0", END)

        for r in records:
            output.insert(END, f"ID:{r[0]} | {r[1]} {r[2]} | {r[3]}\n")

        output.config(state=DISABLED)

    def update_student():
        if id_box.get() == "":
            messagebox.showerror("Error", "Enter ID")
            return

        conn = get_connection()
        c = conn.cursor()
        c.execute("""
            UPDATE student
            SET first_name=?, last_name=?, address=?
            WHERE rowid=?
        """, (f_name.get(), l_name.get(), address.get(), id_box.get()))

        conn.commit()
        conn.close()

        messagebox.showinfo("Updated", "Student Updated")
        clear_fields()
        show_records()

    def delete_student():
        if id_box.get() == "":
            messagebox.showerror("Error", "Enter ID")
            return

        conn = get_connection()
        c = conn.cursor()
        c.execute("DELETE FROM student WHERE rowid=?", (id_box.get(),))
        conn.commit()
        conn.close()

        messagebox.showinfo("Deleted", "Student Deleted")
        clear_fields()
        show_records()

    def clear_fields():
        f_name.delete(0, END)
        l_name.delete(0, END)
        address.delete(0, END)
        id_box.delete(0, END)

    # Main Window
    root = Tk()
    root.title("Student Management System")
    root.geometry("600x650")
    root.configure(bg="#2c3e50")

    Label(root, text="Student Management System",
          font=("Segoe UI", 14, "bold"),
          bg="#2c3e50", fg="white").pack(pady=10)

    Label(root, text="First Name", bg="#2c3e50", fg="white").pack()
    f_name = Entry(root, width=40)
    f_name.pack(pady=5)

    Label(root, text="Last Name", bg="#2c3e50", fg="white").pack()
    l_name = Entry(root, width=40)
    l_name.pack(pady=5)

    Label(root, text="Address", bg="#2c3e50", fg="white").pack()
    address = Entry(root, width=40)
    address.pack(pady=5)

    Label(root, text="Student ID (Update/Delete)",
          bg="#2c3e50", fg="white").pack(pady=5)

    id_box = Entry(root, width=40)
    id_box.pack()

    Button(root, text="Add Student",
           width=35, bg="#1abc9c",
           command=add_student).pack(pady=5)

    Button(root, text="Update Student",
           width=35, bg="#f39c12",
           command=update_student).pack(pady=5)

    Button(root, text="Delete Student",
           width=35, bg="#e74c3c",
           fg="white",
           command=delete_student).pack(pady=5)

    frame = Frame(root)
    frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

    scrollbar = Scrollbar(frame)
    scrollbar.pack(side=RIGHT, fill=Y)

    output = Text(frame, state=DISABLED,
                  yscrollcommand=scrollbar.set)
    output.pack(side=LEFT, fill=BOTH, expand=True)

    scrollbar.config(command=output.yview)

    show_records()
    root.mainloop()


login_window.mainloop()