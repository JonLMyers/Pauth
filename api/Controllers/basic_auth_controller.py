from api.models import User, db
from flask import Blueprint, flash, redirect, request, url_for, jsonify, abort

# Instantiating the Blueprint object
basic_auth_controller = Blueprint('basic_auth_controller', __name__,
                 template_folder='templates')

#######################################
#           Create a new user         #
#######################################
@basic_auth_controller.route('/users', methods = ['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400) # missing arguments

    if User.query.filter_by(username = username).first() is not None:
        abort(400) # existing user

    user = User(username = username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({ 'username': user.username }), 201