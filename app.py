from flask import Flask, request, render_template, url_for, redirect, session, flash
from service import account_service, word_service, init_service

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
_WORD_COUNTING_HTML = "word-counting.html"
_WORD_TABLE_HTML = "word-table.html"

_ERROR = "error"
_INVALID_USERNAME = "Error: the username is invalid. Check the conditions!"
_INVALID_PASSWORD = "Error: the password is invalid. Check the conditions!"
_INVALID_EMAIL = "Error: the email is invalid. Use a valid e-mail address!"
_EXISTING_EMAIL = "Error: this e-mail address is already in use. Choose an other!"
_MISMATCHING_PASSWORD = "Error: the password and the confirmed password are not the same!"

_SUCCESS = "success"
_SUCCESSFUL_REG = "Your registration was successful!"

app = Flask(__name__)
app.secret_key = "qfV0ekN^e&r8!7PR"


@app.route(_INDEX_PAGE_URL)
def index():
    return render_template(_INDEX_HTML)


@app.route(_REGISTRATION_PAGE_URL, defaults={"user_name": "", "email": ""})
@app.route(_REGISTRATION_PAGE_URL + "/<user_name>/<email>")
def registration_page(user_name, email):
    return render_template(_REGISTRATION_HTML, user_name=user_name, email=email)


@app.route(_REGISTRATE_URL, methods=["POST"])
def registrate():
    user_name = request.form["user_name"]
    password = request.form["password"]
    email = request.form["email"]
    confirmed_pwd = request.form["confirmed_pwd"]
    user_name_is_ok = _check_reg_user_name(user_name)
    password_is_ok = _check_reg_password(password)
    password_is_confirmed = _check_confirmed_pwd(password, confirmed_pwd)
    email_is_ok = _check_reg_email(email)
    if user_name_is_ok and password_is_ok and password_is_confirmed and email_is_ok:
        email_is_new = _check_email_in_db(email)
        if email_is_new:
            account_service.registrate(user_name, email, password)
            flash(_SUCCESSFUL_REG, _SUCCESS)
            return redirect(_INDEX_PAGE_URL)
    return redirect(_REGISTRATION_PAGE_URL + "/" + str(user_name) + "/" + str(email))


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
            flash("Error: text had invalid characters!", _ERROR)
            return redirect(_WORD_SAVING_PAGE_URL)
        word_service.save_text(text)
        session["text"] = ""
        flash("The words of the text has been saved successfully!", _SUCCESS)
        return redirect(_WORD_SAVING_PAGE_URL)
    return redirect(_INDEX_PAGE_URL)


@app.route(_WORD_COUNTING_PAGE_URL, defaults={"word": "", "quantity": ""})
@app.route(_WORD_COUNTING_PAGE_URL + "/<word>/<quantity>")
def word_counting_page(word, quantity):
    if "logged_in" in session:
        return render_template(
            _WORD_COUNTING_HTML, user_name=session["user_name"], prev_word=word, word_count=quantity, text=session["text"])
    return redirect(_INDEX_PAGE_URL)


@app.route(_WORD_COUNTING_URL, methods=["POST"])
def count_word():
    if "logged_in" in session:
        word = request.form["word"]
        error = _check_for_empty(word)
        if error is None:
            error = _check_for_invalid_input(word)
        if error is None:
            session["text"] = ""
            quantity = word_service.get_word_count(word)
            return redirect(
                _WORD_COUNTING_PAGE_URL + "/" + str(word) + "/" + str(quantity))
        return error
    return redirect(_INDEX_PAGE_URL)


@app.route(_WORD_TABLE_PAGE_URL)
def word_table_page():
    if "logged_in" in session:
        word_table = word_service.get_word_table()
        return render_template(
            _WORD_TABLE_HTML, user_name=session["user_name"], word_table=word_table)
    return redirect(_INDEX_PAGE_URL)


@app.route(_AUTHENTICATE_URL, methods=["POST"])
def authenticate():
    email = request.form["email"]
    password = request.form["password"]
    account = account_service.find_matching_credentials(email, password)
    if account:
        _fill_session_data(account)
        flash("You were successfully logged in", _SUCCESS)
        return redirect(_WORD_SAVING_PAGE_URL)
    else:
        flash("Email address or Password is incorrect!", _ERROR)
        return redirect(_INDEX_PAGE_URL)


@app.route(_LOG_OUT_URL)
def logout():
    session.clear()
    return redirect(_INDEX_PAGE_URL)


def _fill_session_data(account):
    session["logged_in"] = True
    session["id"] = account[0]
    session["user_name"] = account[1]
    session["text"] = ""


def _check_for_empty(word):
    if word == "":
        session["text"] = ""
        flash("Error: the input is empty!", _ERROR)
        return redirect(_WORD_COUNTING_PAGE_URL)


def _check_for_invalid_input(word):
    if word_service.word_has_invalid_characters(word):
        session["text"] = word
        flash("Error: text had invalid characters!", _ERROR)
        return redirect(_WORD_COUNTING_PAGE_URL)


def _check_reg_user_name(user_name):
    return _check_input(word_service.check_user_name, _INVALID_USERNAME, user_name)


def _check_reg_password(password):
    return _check_input(word_service.check_password, _INVALID_PASSWORD, password)


def _check_reg_email(email):
    return _check_input(word_service.check_email, _INVALID_EMAIL, email)


def _check_email_in_db(email):
    return _check_input(word_service.check_email_in_db, _EXISTING_EMAIL, email)


def _check_confirmed_pwd(password, confirmed_pwd):
    return _check_input(word_service.confirm_password, _MISMATCHING_PASSWORD, password, confirmed_pwd)


def _check_input(checker, message, *args):
    accepted = False
    if len(args) == 1:
        accepted = checker(args[0])
    elif len(args) == 2:
        accepted = checker(args[0], args[1])
    if not accepted:
        flash(message, _ERROR)
    return accepted


def setup_app(app):
    init_service.init_db_tables()

setup_app(app)

if __name__ == "__main__":
    app.run(port=5000)
