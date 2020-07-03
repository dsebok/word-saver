from flask import Flask, request, render_template, url_for, redirect, session
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)
app.secret_key = 'qfV0ekN^e&r8!7PR'

app.config['MYSQL_DATABASE_USER'] = 'David'
app.config['MYSQL_DATABASE_PASSWORD'] = '20ential'
app.config['MYSQL_DATABASE_DB'] = 'WordSaver'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/word-saving")
def savingPage():
    return authorizedAccess('saving.html')


@app.route("/word-counting/<word>/<quantity>")
def wordCountingPage(word, quantity):
    if 'loggedin' in session:
        return render_template(
            'word-counting.html', username=session['username'], prevWord=word, wordCount=quantity)
    return redirect("/")


@app.route("/rest-api/count-word", methods=["POST"])
def countWord():
    if 'loggedin' in session:
        word = request.form['word']
        if word == "":
            word = " "
        quantity = getWordCount(word)
        return redirect(
            url_for("wordCountingPage", word=word, quantity=quantity))
    return redirect("/")


@app.route("/word-table")
def wordTablePage():
    return authorizedAccess('word-table.html')


@app.route("/rest-api/dump-words")
def dumpWords():
    return authorizedRedirect("/word-table")


@app.route("/rest-api/authenticate", methods=["POST"])
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
    return redirect("/")


def authorizedAccess(target):
    if 'loggedin' in session:
        return render_template(
            target, username=session['username'])
    return redirect("/")


def authorizedRedirect(target):
    if 'loggedin' in session:
        # do stuff
        return redirect(target)
    return redirect("/")


def authorizedAccess(target):
    if 'loggedin' in session:
        return render_template(
            target, username=session['username'])
    return redirect("/")


def findMatchingCredentials(email, password):
    cursor = mysql.connect().cursor()
    cursor.execute(
        "SELECT * from User where email=%s and password=%s",
        (email,
         password))
    return cursor.fetchone()


def getWordCount(word):
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT quantity FROM word WHERE word=%s", (word))
    quantity = cursor.fetchone()
    if quantity:
        return quantity[0]
    else:
        return 0


if __name__ == "__main__":
    app.run(debug=True)
