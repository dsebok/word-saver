from flask import Flask, request, render_template, url_for
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


@app.route("/Authenticate")
def authenticate():
    username = request.args.get('UserName')
    password = request.args.get('Password')
    cursor = mysql.connect().cursor()
    cursor.execute(
        "SELECT * from User where Username='" +
        username +
        "' and Password='" +
        password +
        "'")
    data = cursor.fetchone()
    if data is None:
        return "Username or Password is wrong"
    else:
        return "Logged in successfully"


if __name__ == "__main__":
    app.run(debug=True)
