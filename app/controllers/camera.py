from flask import Blueprint
from flask import render_template
from app.models.car import Car
from app.models.user import Role
from app.models.config import db

camera = Blueprint('camera', __name__, template_folder='views')

@camera.route("/admin/cameras", methods=["GET"])
def cameras():
    return render_template("cameras.html", current_page="cameras" )
