from tkinter import *
from tkinter import messagebox, ttk
import sqlite3
import time


def connect_db():
    conn = sqlite3.connect("students.db")
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS users(
        username TEXT,
        password TEXT)""")

    c.execute("""CREATE TABLE IF NOT EXISTS student(
        first_name TEXT,
        last_name TEXT,
        address TEXT)""")

    c.execute("SELECT * FROM users WHERE username='admin'")
    if not c.fetchone():
        c.execute("INSERT INTO users VALUES('admin','1234')")

    conn.commit()
    conn.close()

def get_connection():
    return sqlite3.connect("students.db")

connect_db()


root = Tk()
root.title("Student Management System")
root.geometry("1000x600")
root.resizable(False, False)
root.configure(bg="#1f2c3b")


def login():
    username=user_entry.get()
    password=pass_entry.get()

    conn=get_connection()
    c=conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?",(username,password))
    result=c.fetchone()
    conn.close()

    if result:
        login_frame.destroy()
        open_dashboard(username)
    else:
        messagebox.showerror("Error","Invalid Username or Password")


def open_register():
    reg=Toplevel(root)
    reg.title("Register")
    reg.geometry("300x250")

    Label(reg,text="Register",font=("Arial",14,"bold")).pack(pady=10)

    Label(reg,text="Username").pack()
    ru=Entry(reg)
    ru.pack()

    Label(reg,text="Password").pack()
    rp=Entry(reg,show="*")
    rp.pack()

    def save():
        if ru.get()=="" or rp.get()=="":
            messagebox.showerror("Error","All fields required")
            return

        conn=get_connection()
        c=conn.cursor()
        c.execute("INSERT INTO users VALUES (?,?)",(ru.get(),rp.get()))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success","Registration Successful")
        reg.destroy()

    Button(reg,text="Register",command=save).pack(pady=10)


def forgot_password():
    fp=Toplevel(root)
    fp.title("Reset Password")
    fp.geometry("350x250")
    fp.configure(bg="#2c3e50")

    Label(fp,text="Reset Password",font=("Segoe UI",14,"bold"),
          bg="#2c3e50",fg="white").pack(pady=10)

    Label(fp,text="Username",bg="#2c3e50",fg="white").pack()
    u=Entry(fp)
    u.pack()

    Label(fp,text="New Password",bg="#2c3e50",fg="white").pack()
    p=Entry(fp,show="*")
    p.pack()

    def reset():
        conn=get_connection()
        c=conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?",(u.get(),))
        if c.fetchone():
            c.execute("UPDATE users SET password=? WHERE username=?",(p.get(),u.get()))
            conn.commit()
            messagebox.showinfo("Success","Password Updated Successfully")
            fp.destroy()
        else:
            messagebox.showerror("Error","User not found")
        conn.close()

    Button(fp,text="Reset Password",bg="#1abc9c",fg="white",command=reset).pack(pady=15)


def open_dashboard(username):

    header=Frame(root,bg="#2c3e50",height=60)
    header.pack(fill=X)

    Label(header,text=f"Welcome {username}",
          bg="#2c3e50",fg="white",
          font=("Segoe UI",14,"bold")).pack(side=LEFT,padx=20)

    global time_label
    time_label=Label(header,bg="#2c3e50",fg="yellow")
    time_label.pack(side=RIGHT,padx=20)
    update_time()

    menu=Frame(root,bg="#34495e",width=200)
    menu.pack(side=LEFT,fill=Y)

    global main_area
    main_area=Frame(root,bg="#ecf0f1")
    main_area.pack(fill=BOTH,expand=True)

    Button(menu,text="Dashboard",width=20,command=show_dashboard).pack(pady=10)
    Button(menu,text="Manage Students",width=20,command=show_manage).pack(pady=10)
    Button(menu,text="Account",width=20,command=lambda:show_account(username)).pack(pady=10)
    Button(menu,text="Logout",width=20,command=root.destroy).pack(pady=10)

    show_dashboard()


def update_time():
    current=time.strftime("%I:%M:%S %p %d/%m/%Y")
    time_label.config(text=current)
    time_label.after(1000,update_time)


def clear_main():
    for widget in main_area.winfo_children():
        widget.destroy()

def show_dashboard():
    clear_main()
    Label(main_area,text="Dashboard Overview",
          font=("Segoe UI",16,"bold"),
          bg="#ecf0f1").pack(pady=20)

    conn=get_connection()
    c=conn.cursor()
    c.execute("SELECT COUNT(*) FROM student")
    total=c.fetchone()[0]
    conn.close()

    Label(main_area,text=f"Total Students: {total}",
          font=("Segoe UI",14),
          bg="#ecf0f1").pack(pady=10)


def show_manage():
    clear_main()

    global f_name,l_name,address,id_box,tree

    form=Frame(main_area,bg="#ecf0f1")
    form.pack(pady=10)

    Label(form,text="First Name").grid(row=0,column=0)
    f_name=Entry(form); f_name.grid(row=0,column=1)

    Label(form,text="Last Name").grid(row=0,column=2)
    l_name=Entry(form); l_name.grid(row=0,column=3)

    Label(form,text="Address").grid(row=1,column=0)
    address=Entry(form,width=40); address.grid(row=1,column=1,columnspan=3)

    Label(form,text="ID").grid(row=2,column=0)
    id_box=Entry(form); id_box.grid(row=2,column=1)

    Button(form,text="Add",command=add_student).grid(row=3,column=0,pady=5)
    Button(form,text="Update",command=update_student).grid(row=3,column=1)
    Button(form,text="Delete",command=delete_student).grid(row=3,column=2)
    Button(form,text="Clear",command=clear_fields).grid(row=3,column=3)

    table_frame=Frame(main_area)
    table_frame.pack(fill=BOTH,expand=True)

    tree=ttk.Treeview(table_frame,columns=("ID","First","Last","Address"),show="headings")
    for col in ("ID","First","Last","Address"):
        tree.heading(col,text=col)
    tree.pack(fill=BOTH,expand=True)

    tree.bind("<ButtonRelease-1>",select_record)
    refresh_table()

def refresh_table():
    for row in tree.get_children():
        tree.delete(row)

    conn=get_connection()
    c=conn.cursor()
    c.execute("SELECT rowid,* FROM student")
    for row in c.fetchall():
        tree.insert("",END,values=row)
    conn.close()

def select_record(e):
    selected=tree.focus()
    values=tree.item(selected,"values")
    if values:
        id_box.delete(0,END); id_box.insert(0,values[0])
        f_name.delete(0,END); f_name.insert(0,values[1])
        l_name.delete(0,END); l_name.insert(0,values[2])
        address.delete(0,END); address.insert(0,values[3])

def add_student():
    conn=get_connection()
    c=conn.cursor()
    c.execute("INSERT INTO student VALUES (?,?,?)",(f_name.get(),l_name.get(),address.get()))
    conn.commit(); conn.close()
    refresh_table(); clear_fields()

def update_student():
    conn=get_connection()
    c=conn.cursor()
    c.execute("UPDATE student SET first_name=?,last_name=?,address=? WHERE rowid=?",
              (f_name.get(),l_name.get(),address.get(),id_box.get()))
    conn.commit(); conn.close()
    refresh_table(); clear_fields()

def delete_student():
    conn=get_connection()
    c=conn.cursor()
    c.execute("DELETE FROM student WHERE rowid=?",(id_box.get(),))
    conn.commit(); conn.close()
    refresh_table(); clear_fields()

def clear_fields():
    for e in (f_name,l_name,address,id_box):
        e.delete(0,END)

def show_account(username):
    clear_main()
    Label(main_area,text=f"Logged in as: {username}",
          font=("Segoe UI",14),
          bg="#ecf0f1").pack(pady=20)


login_frame=Frame(root,bg="#2c3e50",padx=40,pady=40)
login_frame.place(relx=0.5,rely=0.5,anchor=CENTER)

Label(login_frame,text="Student Management System",
      font=("Segoe UI",16,"bold"),
      bg="#2c3e50",fg="white").pack(pady=10)

Label(login_frame,text="Username",bg="#2c3e50",fg="white").pack()
user_entry=Entry(login_frame); user_entry.pack(pady=5)

Label(login_frame,text="Password",bg="#2c3e50",fg="white").pack()
pass_entry=Entry(login_frame,show="*"); pass_entry.pack(pady=5)

Button(login_frame,text="Login",command=login).pack(pady=10)
Button(login_frame,text="Register",command=open_register).pack()
Button(login_frame,text="Forgot Password",command=forgot_password).pack(pady=5)

root.mainloop()