from flask import Session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import string
import random
from os import urandom
from base64 import b64encode

db = SQLAlchemy()
BCRYPT = Bcrypt()
sess = Session()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(32), index = True)
    password_hash = db.Column(db.String(128))
    session_token = db.Column(db.String(256))

    def hash_password(self, password):
        self.password_hash = BCRYPT.generate_password_hash(password)
        return True

    def verify_password(self, password):
        password = BCRYPT.generate_password_hash(password)
        return BCRYPT.check_password_hash(self.password_hash, password)

    def generate_session_token(self):
        token = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(128))
        return token

    def delete_session_token(self):
        self.session_token = None