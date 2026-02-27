from main import get_connection

def add_student(first, last, address):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO student VALUES (?,?,?)", (first, last, address))
    conn.commit()
    conn.close()


def get_students():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT rowid, * FROM student")
    records = c.fetchall()
    conn.close()
    return records


def update_student(student_id, first, last, address):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        UPDATE student
        SET first_name=?, last_name=?, address=?
        WHERE rowid=?
    """, (first, last, address, student_id))
    conn.commit()
    conn.close()


def delete_student(student_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM student WHERE rowid=?", (student_id,))
    conn.commit()
    conn.close()