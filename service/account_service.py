import hashlib
import binascii
import os
from dao import mysql_dao


def registrate(user_name, email, password):
    pwd_hash = _hash_password(password)
    mysql_dao.registrate(user_name, email, pwd_hash)


def find_matching_credentials(email, password):
    user_info = mysql_dao.get_user_info(email)
    if user_info:
        if _verify_password(user_info[3], password):
            return user_info
        else:
            return False
    return False


def _hash_password(password):
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwd_hash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                   salt, 100000)
    pwd_hash = binascii.hexlify(pwd_hash)
    return (salt + pwd_hash).decode('ascii')


def _verify_password(stored_password, provided_password):
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwd_hash = hashlib.pbkdf2_hmac('sha512',
                                   provided_password.encode('utf-8'),
                                   salt.encode('ascii'),
                                   100000)
    pwd_hash = binascii.hexlify(pwd_hash).decode('ascii')
    return pwd_hash == stored_password
