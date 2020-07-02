from flask import Flask, request, render_template, url_for, redirect
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'David'
app.config['MYSQL_DATABASE_PASSWORD'] = '20ential'
app.config['MYSQL_DATABASE_DB'] = 'WordSaver'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/word-saving")
def wordsaving():
    return render_template("saving.html")


@app.route("/Authenticate", methods=["POST"])
def authenticate():
    email = request.form['email']
    password = request.form['password']
    cursor = mysql.connect().cursor()

    cursor.execute(
        "SELECT * from User where email='" +
        email +
        "' and password='" +
        password +
        "'")
    data = cursor.fetchone()

    if data is None:
        return "Email address or Password is wrong"
    else:
        return redirect("/word-saving")


if __name__ == "__main__":
    app.run(debug=True)
