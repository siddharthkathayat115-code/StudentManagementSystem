from main import get_connection


def check_login(username, password):
    if username.strip() == "" or password.strip() == "":
        return False, "Username and Password required"

    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?",
              (username, password))
    result = c.fetchone()
    conn.close()

    if result:
        return True, "Login Successful"
    else:
        return False, "Invalid Username or Password"



def validate_student(first, last, address):
    if first.strip() == "" or last.strip() == "" or address.strip() == "":
        return False, "All fields are required"
    return True, ""


def validate_id(student_id):
    if student_id.strip() == "":
        return False, "Student ID required"
    if not student_id.isdigit():
        return False, "Student ID must be number"
    return True, ""