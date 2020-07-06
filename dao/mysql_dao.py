from flask import Flask
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'WordSaver'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


def registrate(user_name, email, pwd_hash):
    db = mysql.connect()
    cursor = db.cursor()
    cursor.execute("INSERT INTO user VALUES(default, %s, %s, %s)",
                   (user_name, email, pwd_hash))
    db.commit()


def get_user_info(email):
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT * from User where email= %s", (email))
    return cursor.fetchone()


def get_word_table():
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT * FROM word")
    return cursor.fetchall()


def get_word_count(word):
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT quantity FROM word WHERE content=%s", (word))
    return cursor.fetchone()


def update_word_table(word_list):
    query = _create_query(word_list)
    db = mysql.connect()
    cursor = db.cursor()
    cursor.execute(query)
    db.commit()


def _create_query(word_list):
    start = "INSERT INTO word (id, content, quantity) VALUES"
    mid = _flatten_to_string(word_list)
    query = start + mid + " ON DUPLICATE KEY UPDATE quantity=VALUES(quantity)"
    return query


def _flatten_to_string(word_list):
    mid_query = ""
    for word in word_list:
        mid_query += " (" + str(word[0]) + ", '" + word[1] + "', " + str(word[2]) + "),"
    return mid_query[:-1]
