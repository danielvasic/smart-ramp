from flask import Blueprint, redirect, url_for
from flask import jsonify, request, render_template
from flask_login import login_required, current_user
from app.models.car import Car
from app.models.manufacturer import Manufacturer
from app.models.car_type import CarType
from app.models.user import Role
from app.models.config import db

car = Blueprint('car', __name__, template_folder='views')

@car.route("/admin/cars", methods=["GET"])
def cars():
    return render_template(
                "cars.html", 
                cars = Car.query.all(), 
                manufacturers=Manufacturer.query.all(), 
                car_types=CarType.query.all(), current_page="cars" )

@car.route("/admin/car/add", methods=["POST"])
@login_required
def add():
    car = Car()
    car.platenumber = request.form.get('car-platenumber')
    car.year = request.form.get('car-year')
    car.color = request.form.get('car-color')
    car.user_id = current_user.id
    car.car_type_id = request.form.get('car-type-id')
    db.session.add(car)
    db.session.commit()
    return redirect(url_for("car.cars"))
