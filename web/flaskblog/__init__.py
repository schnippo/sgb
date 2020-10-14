from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


PROPERTIES_PATH = "/home/jonas/git/ssgb/controllers/pwm/properties"

app = Flask(__name__)
app.config['SECRET_KEY'] = '151649418616068fB46C3598083817101d3bCD33'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login' #func name of the route
login_manager.login_message_category = 'info'


from flaskblog import routes