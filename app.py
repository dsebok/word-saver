from flask import Flask, request, render_template, url_for, redirect, session, flash
from service import account_service, word_service


app = Flask(__name__)
app.secret_key = 'qfV0ekN^e&r8!7PR'


@app.route("/")
def index():
    return render_template("index.html")


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
            flash("Error: text had invalid characters!", "error")
            return redirect(url_for("savingPage"))
        word_service.saveText(text)
        session['text'] = ""
        flash("The words of the text has been saved successfully!", "success")
        return redirect(url_for("savingPage"))
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
            flash("Error: text had invalid characters!", "error")
            return redirect(
                url_for("wordCountingPage", word="-", quantity="-"))
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
        flash("You were successfully logged in", "success")
        return redirect("/word-saving")
    else:
        flash("Email address or Password is incorrect!", "error")
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
