import requests
from flask import Blueprint, redirect, url_for
from flask import jsonify, request
from flask_login.utils import login_required
from flask_login import logout_user
from flask import current_app, render_template
from flask_login import current_user, login_required
from app.models import Detection
from app.models import Car
from app.models.config import db

detection = Blueprint('detection', __name__, template_folder='views')

@detection.route("/admin/detections", methods=["GET"])
@login_required
def detections():
    detections = []
    for car in Car.query.filter_by(user_id=current_user.id).all():
        detections.extend(car.detections)
    return render_template("detections.html", detections=detections, current_page="detections")
