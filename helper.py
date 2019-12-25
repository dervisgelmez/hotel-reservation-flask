from flask import *
import connection as db
import hashlib

def is_user(mail,password):
    user = db.is_user(mail, md5hasher(password))
    session_set(user)

def create_user(request):
    message = []
    user = {
        'fname':request.form['f_name'],
        'lname':request.form['l_name'],
        'email':request.form['e_mail'],
        'pass':md5hasher(request.form['f_pass'])
   }
    user_isset = db.check_user(user['email'])
    if('isset' in user_isset):
        message = {'type':'error','message':'Bu mail adresi ile bir kullanici daha onceden tanimlanmis.'}
    else:
        db.create_user(user)
        message = {'type':'success','message':'Kullanici basarili bir sekilde olusturuldu.'}
    return message

def find_reservation(request):
    date = {
        'checkin':request.form['checkin'],
        'checkout':request.form['checkout']
    }
    session_set(date)
    return db.get_hotels(request.form['place'], request.form['room'])

def create_reservation():
    reservartion = {
        'hotel_id' : session_get('h_id'),
        'client_id' : session_get('user_id'),
        'room_id' : session_get('r_id'),
        'price' : session_get('r_price'),
        'checkin' : session_get('checkin'),
        'checkout' : session_get('checkout')
    }
    db.create_reservation(reservartion)

def session_set(array):
    for key in array:
        session[key] = array[key]

def session_get(key):
    if key in session:
        return session[key]
    else:
        return False

def session_unset(array):
    for key in array:
        if key in session:
            session.pop(key)

def session_clear():
    session.clear()


def add_to_basket(request):
    basket = {
        'hotel_id' : request.args.get("hotel"),
        'room_id' : request.args.get("room"),
        'client_id': session_get('user_id'),
        'checkin': session_get('checkin'),
        'checkout' :session_get('checkout')
    }
    data = db.get_basket(basket)
    session_set(data)


def add_hotel(request):
    hotel = {
        'title':request.form['name'],
        'area':request.form['area'],
        'address':request.form['address'],
        'attributes':request.form['attributes'],
        'vote':request.form['vote']
    }
    db.add_hotel(hotel)


def delete_hotel(request):
    hotel_id = request.args.get('id')
    db.delete_hotel(hotel_id)


def md5hasher(data):
    md5hash = hashlib.md5()
    md5hash.update(data)
    return str(md5hash.hexdigest())