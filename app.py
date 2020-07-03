from flask import Flask, request, render_template, url_for, redirect, session
from service import word_service, account_service


app = Flask(__name__)
app.secret_key = 'qfV0ekN^e&r8!7PR'


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
        quantity = word_service.getWordCount(word)
        return redirect(
            url_for("wordCountingPage", word=word, quantity=quantity))
    return redirect("/")


@app.route("/word-table")
def wordTablePage():
    if 'loggedin' in session:
        wordtable = word_service.getWordTable()
        return render_template('word-table.html', wordtable=wordtable)
    return redirect("/")


@app.route("/rest-api/authenticate", methods=["POST"])
def authenticate():
    email = request.form['email']
    password = request.form['password']
    account = account_service.findMatchingCredentials(email, password)
    if account:
        createSession(account)
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


def createSession(account):
    session['loggedin'] = True
    session['id'] = account[0]
    session['username'] = account[1]


if __name__ == "__main__":
    app.run(debug=True)
