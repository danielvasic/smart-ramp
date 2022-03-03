from flask import Blueprint
from flask import request, redirect, url_for
from flask_login.utils import login_required
from app.models.car import Car
from app.models.manufacturer import Manufacturer
from app.models.user import Role
from app.models.config import db

manufacturer = Blueprint('manufacturer', __name__, template_folder='views')

@manufacturer.route("/admin/manufacturers/add", methods=["POST"])
@login_required
def add():
    manufacturer = Manufacturer()
    manufacturer.name = request.form.get('manufacturer-name')
    db.session.add(manufacturer)
    db.session.commit()
    return redirect(url_for("car.cars"))
