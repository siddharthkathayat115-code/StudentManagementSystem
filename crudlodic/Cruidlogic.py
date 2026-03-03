from database import connect_db
import frontend

connect_db()
frontend.start_app()
from database import get_connection

def add_student(first,last,address):
    conn=get_connection()
    c=conn.cursor()
    c.execute("INSERT INTO student VALUES (?,?,?)",(first,last,address))
    conn.commit()
    conn.close()

def update_student(id,first,last,address):
    conn=get_connection()
    c=conn.cursor()
    c.execute("UPDATE student SET first_name=?,last_name=?,address=? WHERE rowid=?",    
              (first,last,address,id))
    conn.commit()
    conn.close()

def delete_student(id):
    conn=get_connection()
    c=conn.cursor()
    c.execute("DELETE FROM student WHERE rowid=?",(id,))
    conn.commit()
    conn.close()

def fetch_students():
    conn=get_connection()
    c=conn.cursor()
    c.execute("SELECT rowid,* FROM student")
    rows=c.fetchall()
    conn.close()
    return rows

