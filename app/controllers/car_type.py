from functools import reduce
from flask import Blueprint
from flask import request, render_template, redirect, url_for
from flask_login.utils import login_required
from app.models.car import Car
from app.models.car_type import CarType
from app.models.user import Role
from app.models.config import db

car_type = Blueprint('car_type', __name__, template_folder='views')

@car_type.route("/admin/car_type/add", methods=["POST"])
@login_required
def add():
    car_type = CarType()
    car_type.name = request.form.get('car-type-name')
    car_type.manufacturer_id = request.form.get('manufacturer-id')
    db.session.add(car_type)
    db.session.commit()
    return redirect(url_for("car.cars"))
