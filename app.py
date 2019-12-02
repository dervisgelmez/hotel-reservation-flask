from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("gallery.html")

@app.errorhandler(404)
def page_not_found(error):
   return render_template('404.html')

if __name__ == "__main__":
    app.run(debug = True)