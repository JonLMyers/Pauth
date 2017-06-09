from api.models import User, db
from flask import Blueprint, flash, redirect, request, url_for, jsonify, abort

# Instantiating the Blueprint object
basic_auth_controller = Blueprint('basic_auth_controller', __name__,
                 template_folder='templates')

#######################################
#           Create a new user         #
#######################################
@basic_auth_controller.route('/register', methods = ['POST'])
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
    return jsonify({ 'Status': 200 }, { 'username': user.username })

#######################################
#         Authenticate a user         #
#######################################
@basic_auth_controller.route('/auth', methods = ['POST'])
def auth_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400) # missing arguments

    all_users = User
    user = User.query.filter_by(username = username).first()
    if user is None:
        abort(400) # invlaid username
    
    result = user.verify_password(password)
    if result is None:
        abort(400) # invalid password

    while True:
        session_token = user.generate_session_token()
        if all_users.query.filter_by(session_token = session_token).scalar() is None:
            break

    user.session_token = session_token
    db.session.add(user)
    db.session.commit()

    return jsonify({ 'Status': 200 }, { 'Session Token': session_token})

#######################################
#         Check Authentication        #
#######################################
@basic_auth_controller.route('/isauthed', methods = ['POST'])
def check_auth():
    session_token = request.json.get('session')
    username = request.json.get('username')

    if session_token is None:
        abort(200) # invlaid session_token

    if username is None:
        abort(200) # invlaid username

    user = User.query.filter_by(username = username).first()
    if user is None:
        abort(400) # No user

    if user.query.filter_by(session_token = session_token).filter_by(username = username).scalar() is None:
        abort(400) # No session exists

    return jsonify({ 'Status': 200 })

#######################################
#           Log user out              #
#######################################
@basic_auth_controller.route('/logout', methods = ['POST'])
def logout():
    session_token = request.json.get('session')
    username = request.json.get('username')

    if session_token is None:
        abort(200) # invlaid session_token

    if username is None:
        abort(200) # invlaid username

    user = User.query.filter_by(username = username).first()
    if user is None:
        abort(400) # No user

    if user.query.filter_by(session_token = session_token).filter_by(username = username).scalar() is None:
        abort(400) # No session exists
    
    user.delete_session_token()
    db.session.add(user)
    db.session.commit()

    return jsonify({ 'Status': 200 })



