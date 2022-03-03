import requests
from flask import Blueprint, redirect, url_for
from flask import jsonify, request
from flask_login.utils import login_required
from flask_login import logout_user
from flask import current_app, render_template
from flask_login import current_user, login_required
from app.models import User
from app.models.config import db

user = Blueprint('user', __name__, template_folder='views')

@user.route("/admin/users", methods=["GET"])
@login_required
def users():
    return render_template("users.html", users = User.query.all(), current_page="users")
