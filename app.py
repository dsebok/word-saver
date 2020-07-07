from flask import Flask, request, render_template, url_for, redirect, session, flash
from service import account_service, word_service

_INDEX_PAGE_URL = "/"
_REGISTRATION_PAGE_URL = "/registrate"
_WORD_SAVING_PAGE_URL = "/word-saving"
_WORD_COUNTING_PAGE_URL = "/word-counting"
_WORD_TABLE_PAGE_URL = "/word-table"

_REGISTRATE_URL = "/rest-api/registrate"
_WORD_SAVING_URL = "/rest-api/save-words"
_WORD_COUNTING_URL = "/rest-api/count-word"
_AUTHENTICATE_URL = "/rest-api/authenticate"
_LOG_OUT_URL = "/logout"

_INDEX_HTML = "index.html"
_REGISTRATION_HTML = "registration.html"
_SAVING_HTML = "saving.html"
_WORD_COUNTING_HTML = 'word-counting.html'
_WORD_TABLE_HTML = 'word-table.html'

app = Flask(__name__)
app.secret_key = "qfV0ekN^e&r8!7PR"


@app.route(_INDEX_PAGE_URL)
def index():
    return render_template(_INDEX_HTML)


@app.route(_REGISTRATION_PAGE_URL)
def registration_page():
    return render_template(_REGISTRATION_HTML)


@app.route(_REGISTRATE_URL, methods=["POST"])
def registrate():
    user_name = request.form["user_name"]
    email = request.form["email"]
    password = request.form["password"]
    account_service.registrate(user_name, email, password)
    flash("Your registration was successful!", "success")
    return redirect(_INDEX_PAGE_URL)


@app.route(_WORD_SAVING_PAGE_URL)
def saving_page():
    if "logged_in" in session:
        return render_template(
            _SAVING_HTML, user_name=session["user_name"], text=session["text"])
    return redirect(_INDEX_PAGE_URL)


@app.route(_WORD_SAVING_URL, methods=["POST"])
def save_words():
    if "logged_in" in session:
        text = request.form["text"]
        if word_service.text_has_invalid_characters(text):
            session["text"] = text
            flash("Error: text had invalid characters!", "error")
            return redirect(_WORD_SAVING_PAGE_URL)
        word_service.save_text(text)
        session["text"] = ""
        flash("The words of the text has been saved successfully!", "success")
        return redirect(_WORD_SAVING_PAGE_URL)
    return redirect(_INDEX_PAGE_URL)


@app.route(_WORD_COUNTING_PAGE_URL + "/<word>/<quantity>")
def word_counting_page(word, quantity):
    if 'logged_in' in session:
        return render_template(
            _WORD_COUNTING_HTML, user_name=session['user_name'], prev_word=word, word_count=quantity, text=session["text"])
    return redirect(_INDEX_PAGE_URL)


@app.route(_WORD_COUNTING_URL, methods=["POST"])
def count_word():
    if 'logged_in' in session:
        word = request.form['word']
        error = _check_for_empty(word)
        if error is None:
            error = _check_for_invalid_input(word)
        if error is None:
            session['text'] = ""
            quantity = word_service.get_word_count(word)
            return redirect(
                _WORD_COUNTING_PAGE_URL + "/" + str(word) + "/" + str(quantity))
        return error
    return redirect(_INDEX_PAGE_URL)


@app.route(_WORD_TABLE_PAGE_URL)
def word_table_page():
    if 'logged_in' in session:
        word_table = word_service.get_word_table()
        return render_template(
            _WORD_TABLE_HTML, user_name=session['user_name'], word_table=word_table)
    return redirect(_INDEX_PAGE_URL)


@app.route(_AUTHENTICATE_URL, methods=["POST"])
def authenticate():
    email = request.form['email']
    password = request.form['password']
    account = account_service.find_matching_credentials(email, password)
    if account:
        _create_session(account)
        flash("You were successfully logged in", "success")
        return redirect(_WORD_SAVING_PAGE_URL)
    else:
        flash("Email address or Password is incorrect!", "error")
        return redirect(_INDEX_PAGE_URL)


@app.route(_LOG_OUT_URL)
def logout():
    session.clear()
    return redirect(_INDEX_PAGE_URL)


def _create_session(account):
    session["logged_in"] = True
    session["id"] = account[0]
    session["user_name"] = account[1]
    session["text"] = ""


def _check_for_empty(word):
    if word == "":
        session['text'] = ""
        flash("Error: the input is empty!", "error")
        return redirect(_WORD_COUNTING_PAGE_URL + "/-/-")


def _check_for_invalid_input(word):
    if word_service.word_has_invalid_characters(word):
        session['text'] = word
        flash("Error: text had invalid characters!", "error")
        return redirect(_WORD_COUNTING_PAGE_URL + "/-/-")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
