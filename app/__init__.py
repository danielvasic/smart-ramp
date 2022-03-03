from flask import Flask, url_for, redirect, request, render_template, g, session, send_from_directory
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, current_user
from app.models import db, MYSQL_CONFIG_URI, User, Role
from app.controllers.car import car
from app.controllers.user import user
from app.controllers.camera import camera
from app.controllers.manufacturer import manufacturer
from app.controllers.car_type import car_type
from app.controllers.detection import detection
from app.sso.auth import auth
import os

login_manager = LoginManager()
app = Flask(__name__, template_folder='views', static_url_path='/static')
login_manager.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = MYSQL_CONFIG_URI
app.config['SQLALCHEMY_POOL_RECYCLE'] = 299
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "SmartCampus1!"
PATH = os.path.dirname(os.path.realpath(__file__))

app.register_blueprint(car)
app.register_blueprint(user)
app.register_blueprint(camera)
app.register_blueprint(manufacturer)
app.register_blueprint(car_type)
app.register_blueprint(auth)
app.register_blueprint(detection)

db.init_app(app)
with app.app_context():
    db.create_all()

migrate = Migrate(app, db)

@login_manager.user_loader
def load_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    return user

@app.before_request
def load_user():
    g.user = current_user

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for("user.users"))
    else:
        return redirect(url_for("auth.saml_login"))