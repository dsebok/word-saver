from flask import Flask, request, render_template, url_for, redirect, session, flash
from service import account_service, word_service


app = Flask(__name__)
app.secret_key = "qfV0ekN^e&r8!7PR"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/registrate")
def registration_page():
    return render_template("registration.html")


@app.route("/rest-api/registrate", methods=["POST"])
def registrate():
    user_name = request.form["user_name"]
    email = request.form["email"]
    password = request.form["password"]
    account_service.registrate(user_name, email, password)
    flash("Your registration was successful!", "success")
    return redirect(url_for("index"))


@app.route("/word-saving")
def saving_page():
    if "logged_in" in session:
        return render_template(
            "saving.html", user_name=session["user_name"], text=session["text"])
    return redirect(url_for("index"))


@app.route("/rest-api/save-words", methods=["POST"])
def save_words():
    if "logged_in" in session:
        text = request.form["text"]
        if word_service.text_has_invalid_characters(text):
            session["text"] = text
            flash("Error: text had invalid characters!", "error")
            return redirect(url_for("saving_page"))
        word_service.save_text(text)
        session["text"] = ""
        flash("The words of the text has been saved successfully!", "success")
        return redirect(url_for("saving_page"))
    return redirect(url_for("index"))


@app.route("/word-counting/<word>/<quantity>")
def word_counting_page(word, quantity):
    if 'logged_in' in session:
        return render_template(
            'word-counting.html', user_name=session['user_name'], prev_word=word, word_count=quantity, text=session["text"])
    return redirect(url_for("index"))


@app.route("/rest-api/count-word", methods=["POST"])
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
                url_for("word_counting_page", word=word, quantity=quantity))
        return error
    return redirect(url_for("index"))


@app.route("/word-table")
def word_table_page():
    if 'logged_in' in session:
        word_table = word_service.get_word_table()
        return render_template(
            'word-table.html', user_name=session['user_name'], word_table=word_table)
    return redirect(url_for("index"))


@app.route("/rest-api/authenticate", methods=["POST"])
def authenticate():
    email = request.form['email']
    password = request.form['password']
    account = account_service.find_matching_credentials(email, password)
    if account:
        _create_session(account)
        flash("You were successfully logged in", "success")
        return redirect(url_for("saving_page"))
    else:
        flash("Email address or Password is incorrect!", "error")
        return redirect(url_for("index"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


def _create_session(account):
    session["logged_in"] = True
    session["id"] = account[0]
    session["user_name"] = account[1]
    session["text"] = ""


def _check_for_empty(word):
    if word == "":
        session['text'] = ""
        flash("Error: the input is empty!", "error")
        return redirect(
            url_for("word_counting_page", word="-", quantity="-"))


def _check_for_invalid_input(word):
    if word_service.word_has_invalid_characters(word):
        session['text'] = word
        flash("Error: text had invalid characters!", "error")
        return redirect(
            url_for("word_counting_page", word="-", quantity="-"))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
