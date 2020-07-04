from flask import Flask
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'WordSaver'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


def findMatchingCredentials(email, password):
    cursor = mysql.connect().cursor()
    cursor.execute(
        "SELECT * from User where email=%s and password=%s",
        (email,
         password))
    return cursor.fetchone()


def getWordTable():
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT * FROM word")
    return cursor.fetchall()


def getWordCount(word):
    cursor = mysql.connect().cursor()
    cursor.execute(
        "SELECT quantity FROM word WHERE content=%s",
        (word))
    return cursor.fetchone()


def updateWordTable(wordList):
    query = createQuery(wordList)
    db = mysql.connect()
    cursor = db.cursor()
    cursor.execute(query)
    db.commit()


def createQuery(wordList):
    start = "INSERT INTO word (id, content, quantity) VALUES"
    mid = flattenToString(wordList)
    query = start + mid + " ON DUPLICATE KEY UPDATE quantity=VALUES(quantity)"
    return query


def flattenToString(wordList):
    midQuery = ""
    for word in wordList:
        midQuery += " (" + str(word[0]) + ", '" + word[1] + "', " + str(word[2]) + "),"
    return midQuery[:-1]
