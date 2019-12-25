from flask import *
from datetime import date
import helper
import connection as db

app = Flask(__name__)

@app.route("/")
@app.route("/index.html")
def index():
    return render_template("app/index.html")

@app.route("/reservation", methods=['POST'])
def reservation():
    hotels = helper.find_reservation(request)
    return render_template("app/reservation.html", hotels=hotels)


@app.route("/about")
def about():
    return render_template("app/aboutus.html")

@app.route("/login", methods=['POST','GET'])
def login():
    if request.method=='POST':
        email = request.form['email']
        password = request.form['password']
        helper.is_user(email,password)
    else:
        return page_not_found(404)
    return render_template("app/index.html")

@app.route("/logout", methods=['POST','GET'])
def logout():
    helper.session_clear()
    return render_template("app/index.html")

@app.route("/signup", methods=['POST','GET'])
def signup():
    if request.method=='POST':
        message = helper.create_user(request)
        return render_template("app/index.html", alert=message)
    else:
        return page_not_found(404)

@app.route("/contact")
def contact():
    return render_template("app/contact.html")

@app.route("/basket")
def basket():
    return render_template("app/basket.html")

@app.route("/add-to-basket", methods=['GET'])
def add_to_basket():
    helper.add_to_basket(request)
    return render_template("app/basket.html")

@app.route("/user")
def user():
    return render_template("app/contact.html")

@app.route("/basket-clear")
def basket_clear():
    basket = {'basket','h_id','h_area_code','h_title','h_address','h_attributes','r_id','r_title','r_attributes','r_price','r_rank','h_location'}
    helper.session_unset(basket)
    return render_template("app/index.html")

@app.route("/reservation/create")
def create_reservation():
    if helper.session_get('basket'):
        helper.create_reservation()
        return basket_clear()
    else:
        return page_not_found(404)


@app.route("/admin")
@app.route("/admin.html")
def admin():
    roles = helper.session_get('user_roles')
    if (roles != "admin"):
        return index()
    return render_template("admin/index.html")

@app.route("/admin/hotel")
def a_hotel():
    roles = helper.session_get('user_roles')
    if (roles != "admin"):
        return index()
    hotels = db.get_all_hotels()
    areas = db.get_all_areas()
    return render_template("admin/hotel.html", hotels = hotels, areas=areas)

@app.route("/admin/hotel", methods=['POST'])
def add_hotel():
    roles = helper.session_get('user_roles')
    if (roles != "admin"):
        return index()
    if request.method=='POST':
        helper.add_hotel(request)
        return a_hotel()
    else:
        return page_not_found(404)

@app.route("/admin/hotel/delete")
def delete_hotel():
    roles = helper.session_get('user_roles')
    if (roles != "admin"):
        return index()
    helper.delete_hotel(request)
    return a_hotel()

@app.errorhandler(404)
def page_not_found(error):
   return render_template('404.html')

if __name__ == "__main__":
    app.secret_key = helper.md5hasher(str(date.today()))
    app.run(debug = True)