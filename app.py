from flask import Flask, request, render_template, url_for, redirect, session
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)
app.secret_key = 'JahIthBer2000'

app.config['MYSQL_DATABASE_USER'] = 'David'
app.config['MYSQL_DATABASE_PASSWORD'] = '20ential'
app.config['MYSQL_DATABASE_DB'] = 'WordSaver'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/word-saving")
def save():
    if 'loggedin' in session:
        return render_template(
            'saving.html', username=session['username'])
    return redirect("/")


@app.route("/Authenticate", methods=["POST"])
def authenticate():
    email = request.form['email']
    password = request.form['password']
    account = findMatchingCredentials(email, password)
    if account:
        session['loggedin'] = True
        session['id'] = account[0]
        session['username'] = account[1]
        return redirect("/word-saving")
    else:
        return "Email address or Password is incorrect!"


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    # Redirect to login page
    return redirect("/")


def findMatchingCredentials(email, password):
    cursor = mysql.connect().cursor()
    cursor.execute(
        "SELECT * from User where email=%s and password=%s",
        (email,
         password))
    return cursor.fetchone()


if __name__ == "__main__":
    app.run(debug=True)
