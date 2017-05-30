from app import BCRYPT, DB
from app.models import User
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask.ext.sqlalchemy import SQLAlchemy

# Instantiating the Blueprint object
BASIC = Blueprint('basic_auth_controller', __name__,
                 template_folder='templates',
                 static_folder='static')

@app.route('/users', methods = ['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400) # missing arguments

    if User.query.filter_by(username = username).first() is not None:
        abort(400) # existing user

    user = User(username = username)
    user.hash_password(password)
    DB.session.add(user)
    DB.session.commit()
    return jsonify({ 'username': user.username }), 201, {'Location': url_for('get_user', id = user.id, _external = True)}