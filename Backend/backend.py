from database import get_connection

def login_user(username,password):
    conn=get_connection()
    c=conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?",(username,password))
    result=c.fetchone()
    conn.close()
    return result

def register_user(username,password):
    conn=get_connection()
    c=conn.cursor()
    c.execute("INSERT INTO users VALUES (?,?)",(username,password))
    conn.commit()
    conn.close()

def reset_password(username,newpass):
    conn=get_connection()
    c=conn.cursor()
    c.execute("UPDATE users SET password=? WHERE username=?",(newpass,username))
    conn.commit()
    conn.close()



