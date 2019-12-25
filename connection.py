import mysql.connector
from datetime import date

con = mysql.connector.connect(user='root', password='root', host='127.0.0.1', database='cinar')

def is_user(mail,password):
    user = []
    c = con.cursor()
    c.execute("SELECT * FROM client WHERE email='"+mail+"' AND password='"+password+"'")
    for row in c:
        user = {
            'login': 'on',
            'user_id': str(row[0]),
            'user_name':row[1]+" "+row[2],
            'user_email': row[4],
            'user_roles': row[5]
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

def get_areas_code(value):
    area = []
    c = con.cursor()
    c.execute("SELECT * FROM area WHERE city='"+value+"'")
    for row in c:
        area = str(row[0])
    return area

def get_hotels(value, room="0"):
    area_code = get_areas_code(value)
    hotels = []
    c = con.cursor(buffered=True)
    c.execute("SELECT * FROM hotel WHERE area_code='"+area_code+"'")
    for row in c:
        hotel = {
            'id': str(row[0]),
            'title': row[1],
            'address' : row[3],
            'attributes' : row[4],
            'vote' : str(row[5]),
            'img' : row[6],
            'rooms' : get_rooms(row[0], room)
        }
        hotels.append(hotel)
    return hotels


def get_rooms(value, rank):
    rooms = []
    c = con.cursor(buffered=True)
    if (rank == "0"):
        c.execute("SELECT * FROM room WHERE hotel_id='"+str(value)+"'")
    else:
        c.execute("SELECT * FROM room WHERE hotel_id='"+str(value)+"' AND room_rank='"+str(rank)+"'")
    for row in c:
        room = {
            'id':str(row[0]),
            'title': row[2],
            'attributes': row[3],
            'price':row[4],
            'rank':str(row[5])
        }
        rooms.append(room)
    return rooms

def get_room_by_id(value):
    room = []
    c = con.cursor(buffered=True)
    c.execute("SELECT * FROM room WHERE id='"+value+"'")
    for row in c:
        room = {
            'r_id':str(row[0]),
            'r_title': row[2],
            'r_attributes': row[3],
            'r_price':row[4],
            'r_rank':str(row[5])
        }
    return room

def get_area_by_id(value):
    area = []
    c = con.cursor(buffered=True)
    c.execute("SELECT * FROM area WHERE area_code='"+value+"'")
    for row in c:
        area = {
            'h_location':row[2]+", "+row[1]
        }
    return area

def create_user(user):
    c = con.cursor()
    record = [user['fname'], user['lname'], user['pass'], user['email'],'user']
    c.execute("insert into client(first_name, last_name, password, email, roles) values(%s,%s,%s,%s,%s)", record)
    con.commit()

def get_basket(basket):
    hotel = []
    c = con.cursor(buffered=True)
    c.execute("SELECT * FROM hotel WHERE id='"+basket['hotel_id']+"'")
    for row in c:
        hotel = {
            'basket': 'on',
            'h_id': str(row[0]),
            'h_area_code': str(row[2]),
            'h_title': row[1],
            'h_address' : row[3],
            'h_attributes' : row[4],
            'h_img': row[6]
        }
    data = hotel.copy()
    data.update(get_room_by_id(basket['room_id']))
    data.update(get_area_by_id(hotel['h_area_code']))
    return data


def get_all_hotels():
    hotels = []
    c = con.cursor(buffered=True)
    c.execute("SELECT * FROM hotel")
    for row in c:
        hotel = {
            'id': str(row[0]),
            'title': row[1],
            'address' : row[3],
            'attributes' : row[4],
            'vote' : str(row[5])
        }
        data = hotel.copy()
        data.update(get_area_by_id(str(row[2])))
        hotels.append(data)
    return hotels

def get_all_areas():
    areas = []
    c = con.cursor(buffered=True)
    c.execute("SELECT * FROM area")
    for row in c:
        area = {
            'id': str(row[0]),
            'title': row[2]+", "+row[1]
        }
        areas.append(area)
    return areas

def add_hotel(hotel):
    c = con.cursor()
    record = [hotel['title'], hotel['area'], hotel['address'], hotel['attributes'], hotel['vote']]
    c.execute("insert into hotel(title, area_code, address, hotel_attributes, vote) values(%s,%s,%s,%s,%s)", record)
    con.commit()


def delete_hotel(param):
    c = con.cursor()
    c.execute("Delete from hotel where id ='"+param+"'")
    con.commit()

def create_reservation(data):
    c = con.cursor()
    record = [data['hotel_id'], data['client_id'], data['room_id'], data['price'],'reservation',data['checkin'], data['checkout'], date.today()]
    c.execute("insert into reservation(hotel_id, client_id, rooms_id, price, status, check_in_date, check_out_date, created_at) values(%s,%s,%s,%s,%s,%s,%s,%s)", record)
    con.commit()
