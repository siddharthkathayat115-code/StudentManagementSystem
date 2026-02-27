from tkinter import *
from tkinter import messagebox, ttk
from backend import login_user, register_user, reset_password
from crud_logic import add_student, update_student, delete_student, fetch_students


def login_screen(root, open_dashboard):

    frame=Frame(root,bg="#2c3e50",padx=40,pady=40)
    frame.place(relx=0.5,rely=0.5,anchor=CENTER)

    Label(frame,text="Student Management System",
          font=("Segoe UI",16,"bold"),
          bg="#2c3e50",fg="white").pack(pady=10)

    Label(frame,text="Username",bg="#2c3e50",fg="white").pack()
    user=Entry(frame); user.pack()

    Label(frame,text="Password",bg="#2c3e50",fg="white").pack()
    pas=Entry(frame,show="*"); pas.pack()

    def do_login():
        if login_user(user.get(),pas.get()):
            frame.destroy()
            open_dashboard(user.get())
        else:
            messagebox.showerror("Error","Invalid Username or Password")

    Button(frame,text="Login",command=do_login).pack(pady=10)
    Button(frame,text="Register",command=lambda:register_window(root)).pack()
    Button(frame,text="Forgot Password",command=lambda:reset_window(root)).pack()

def register_window(root):
    w=Toplevel(root)
    w.title("Register")
    w.geometry("300x250")

    u=Entry(w); u.pack(pady=10)
    p=Entry(w,show="*"); p.pack()

    Button(w,text="Register",
           command=lambda:(register_user(u.get(),p.get()),w.destroy())
    ).pack(pady=10)


def reset_window(root):
    w=Toplevel(root)
    w.title("Reset Password")
    w.geometry("300x250")

    u=Entry(w); u.pack(pady=10)
    p=Entry(w,show="*"); p.pack()

    Button(w,text="Reset",
           command=lambda:(reset_password(u.get(),p.get()),w.destroy())
    ).pack(pady=10)


def dashboard(root,username):

    for w in root.winfo_children():
        w.destroy()

    Label(root,text=f"Welcome {username}",font=("Arial",16)).pack(pady=10)

    Button(root,text="Manage Students",
           command=lambda:manage_students(root)).pack(pady=10)


def manage_students(root):

    for w in root.winfo_children():
        w.destroy()

    f=Entry(root); f.pack()
    l=Entry(root); l.pack()
    a=Entry(root); a.pack()
    i=Entry(root); i.pack()

    Button(root,text="Add",
           command=lambda:add_student(f.get(),l.get(),a.get())).pack()
    Button(root,text="Update",
           command=lambda:update_student(i.get(),f.get(),l.get(),a.get())).pack()
    Button(root,text="Delete",
           command=lambda:delete_student(i.get())).pack()

    tree=ttk.Treeview(root,columns=("ID","First","Last","Address"),show="headings")
    for col in ("ID","First","Last","Address"):
        tree.heading(col,text=col)
    tree.pack()

    for row in fetch_students():
        tree.insert("",END,values=row)