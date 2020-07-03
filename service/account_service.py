from dao import mysql_dao


def findMatchingCredentials(email, password):
    return mysql_dao.findMatchingCredentials(email, password)
