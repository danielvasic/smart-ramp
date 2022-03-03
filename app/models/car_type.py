from app.models.config import db
from sqlalchemy.orm import relationship 

class CarType(db.Model):
    __tablename__="car_type"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(25), nullable=False)
    cars = relationship("Car", back_populates="car_type")
    manufacturer_id = db.Column(db.Integer, db.ForeignKey("manufacturer.id"))
    manufacturer = relationship("Manufacturer", back_populates="car_types")