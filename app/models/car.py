from app.models.config import db
from sqlalchemy.orm import relationship 

class Car (db.Model):
    __tablename__ = "car"
    platenumber = db.Column(db.String(20), primary_key=True)
    color = db.Column(db.String(20), nullable=True)
    year = db.Column(db.String(6), nullable=True)
    car_type_id = db.Column(db.Integer, db.ForeignKey("car_type.id"))
    car_type = relationship("CarType", back_populates="cars")
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    user = relationship("User", back_populates="cars")
    detections = relationship("Detection", back_populates="car")