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
    return render_template("app/reservation.html")
    return helper.find_reservation(request)





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





@app.errorhandler(404)
def page_not_found(error):
   return render_template('404.html')







if __name__ == "__main__":
    app.secret_key = helper.md5hasher(str(date.today()))
    app.run(debug = True)