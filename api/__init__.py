#!flask/bin/python
from flask import Flask

app = Flask(__name__)

# Set default config values (app.config)
# Later we should useinstance-specific values (app.instance.config)
app.config.from_pyfile(app.root_path + '/config.py')

from api.models import db
db.init_app(app)

from api.Controllers.basic_auth_controller import basic_auth_controller
app.register_blueprint(basic_auth_controller, url_prefix='/basic')