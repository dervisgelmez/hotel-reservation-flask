import mysql.connector

con = mysql.connector.connect(user='root', password='root', host='127.0.0.1', database='cinar')

def is_user(mail,password):
    user = []
    c = con.cursor()
    c.execute("SELECT * FROM client WHERE email='"+mail+"' AND password='"+password+"'")
    for row in c:
        user = {
            'login': 'on',
            'id': str(row[0]),
            'name':row[1]+" "+row[2],
            'email': row[4],
            'roles': row[5]
        }
    return user

def check_user(mail):
    user = []
    c = con.cursor()
    c.execute("SELECT * FROM client WHERE email='"+mail+"'")
    for row in c:
        user = {
            'isset': 'true',
        }
    return user

def get_areas():
    return "q"


def create_user(user):
    c = con.cursor()
    record = [user['fname'], user['lname'], user['pass'], user['email'],'user']
    c.execute("insert into client(first_name, last_name, password, email, roles) values(%s,%s,%s,%s,%s)", record)
    con.commit()