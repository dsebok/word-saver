from dao import mysql_dao


def init_db_tables():
    mysql_dao.init_user_table()
    mysql_dao.init_word_table()
