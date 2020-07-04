from flask import Flask, request, render_template, url_for, redirect, session
from service import account_service, word_service


app = Flask(__name__)
app.secret_key = 'qfV0ekN^e&r8!7PR'


@app.route("/")
def index():
    if not session.get('error'):
        session['error'] = ""
    return render_template("index.html", errorMsg=session['error'])


@app.route("/word-saving")
def savingPage():
    if 'loggedin' in session:
        return render_template(
            'saving.html', username=session['username'], text=session['text'])
    return redirect("/")


@app.route("/rest-api/save-words", methods=["POST"])
def saveWords():
    if 'loggedin' in session:
        text = request.form['text']
        if word_service.textHasInvalidCharacters(text):
            session['text'] = text
            return redirect(url_for("savingPage"))
            # add error msg
        word_service.saveText(text)
        session['text'] = ""
        return redirect(url_for("savingPage"))
        # add success msg
    return redirect("/")


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
        if word_service.wordHasInvalidCharacters(word):
            return redirect(
                url_for("wordCountingPage", word="-", quantity="-"))
            # redirect banner for typing in sg
        quantity = word_service.getWordCount(word)
        return redirect(
            url_for("wordCountingPage", word=word, quantity=quantity))
    return redirect("/")


@app.route("/word-table")
def wordTablePage():
    if 'loggedin' in session:
        wordtable = word_service.getWordTable()
        return render_template(
            'word-table.html', username=session['username'], wordtable=wordtable)
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
        session['error'] = "Email address or Password is incorrect!"
        return redirect("/")


@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")


def createSession(account):
    session['loggedin'] = True
    session['id'] = account[0]
    session['username'] = account[1]
    session['text'] = ""


if __name__ == "__main__":
    app.run(debug=True)
