from tkinter import *
from tkinter import messagebox
import sqlite3



def connect_db():
    conn = sqlite3.connect("student_records.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS student (
            first_name TEXT,
            last_name TEXT,
            address TEXT
        )
    """)
    conn.commit()
    conn.close()


def get_connection():
    return sqlite3.connect("student_records.db")



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
    c.execute(
        "INSERT INTO student VALUES (?,?,?)",
        (f_name.get(), l_name.get(), address.get())
    )
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Student Added Successfully")
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
        output.insert(
            END,
            f"ID: {r[0]} | {r[1]} {r[2]} | {r[3]}\n"
        )

    output.config(state=DISABLED)


def auto_fill(event=None):
    if id_box.get() == "":
        return

    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM student WHERE rowid=?", (id_box.get(),))
    record = c.fetchone()
    conn.close()

    if record:
        f_name.delete(0, END)
        l_name.delete(0, END)
        address.delete(0, END)

        f_name.insert(0, record[0])
        l_name.insert(0, record[1])
        address.insert(0, record[2])



def update_student():
    if id_box.get() == "":
        messagebox.showerror("Error", "Enter ID to update")
        return

    if not validate_fields():
        return

    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        UPDATE student
        SET first_name=?, last_name=?, address=?
        WHERE rowid=?
    """, (f_name.get(), l_name.get(), address.get(), id_box.get()))

    if c.rowcount == 0:
        messagebox.showerror("Error", "No record found with this ID")
        conn.close()
        return

    conn.commit()
    conn.close()

    messagebox.showinfo("Updated", "Student Updated Successfully")
    clear_fields()
    show_records()



def delete_student():
    if id_box.get() == "":
        messagebox.showerror("Error", "Enter ID to delete")
        return

    if not messagebox.askyesno("Confirm", "Are you sure you want to delete this student?"):
        return

    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM student WHERE rowid=?", (id_box.get(),))

    if c.rowcount == 0:
        messagebox.showerror("Error", "No record found with this ID")
        conn.close()
        return

    conn.commit()
    conn.close()

    messagebox.showinfo("Deleted", "Student Deleted Successfully")
    clear_fields()
    show_records()



def clear_fields():
    f_name.delete(0, END)
    l_name.delete(0, END)
    address.delete(0, END)
    id_box.delete(0, END)



connect_db()

root = Tk()
root.title("Student Management System")
root.geometry("600x700")
root.resizable(True, True)
root.configure(bg="#2c3e50")

Label(
    root,
    text="Student Management System",
    font=("Segoe UI", 14, "bold"),
    bg="#2c3e50",
    fg="white"
).pack(pady=10)

Label(root, text="First Name", bg="#2c3e50", fg="white").pack()
f_name = Entry(root, width=40)
f_name.pack(pady=5)

Label(root, text="Last Name", bg="#2c3e50", fg="white").pack()
l_name = Entry(root, width=40)
l_name.pack(pady=5)

Label(root, text="Address", bg="#2c3e50", fg="white").pack()
address = Entry(root, width=40)
address.pack(pady=5)

Label(
    root,
    text="Student ID (for Update / Delete)",
    bg="#2c3e50",
    fg="white"
).pack(pady=5)

id_box = Entry(root, width=40)
id_box.pack()
id_box.bind("<FocusOut>", auto_fill)

Button(
    root,
    text="Add Student",
    width=35,
    bg="#1abc9c",
    command=add_student
).pack(pady=5)

Button(
    root,
    text="Update Student",
    width=35,
    bg="#f39c12",
    command=update_student
).pack(pady=5)

Button(
    root,
    text="Delete Student",
    width=35,
    bg="#e74c3c",
    fg="white",
    command=delete_student
).pack(pady=5)


# -------------------- OUTPUT (FULL SCREEN WITH SCROLLBAR) --------------------
frame = Frame(root)
frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

scrollbar = Scrollbar(frame)
scrollbar.pack(side=RIGHT, fill=Y)

output = Text(
    frame,
    state=DISABLED,
    yscrollcommand=scrollbar.set
)
output.pack(side=LEFT, fill=BOTH, expand=True)

scrollbar.config(command=output.yview)


show_records()
root.mainloop()
