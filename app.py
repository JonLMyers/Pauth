#!flask/bin/python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)

# Set default config values (app.config)
# Later we should useinstance-specific values (app.instance.config)
app.config.from_pyfile(app.root_path + '/config.py')
DB = SQLAlchemy(app)
BCRYPT = Bcrypt(app)

from app.Controllers.basic_auth_controller import BASIC
app.register_blueprint(BASIC, url_prefix='/basic')