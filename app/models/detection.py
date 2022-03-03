from sqlalchemy.orm import relationship
from app.models.config import db
from datetime import datetime

class Detection (db.Model):
    __tablename__ = "detection"
    id = db.Column(db.Integer, primary_key=True)
    detected_at = db.Column(db.DateTime, nullable=True,default=datetime.utcnow)
    entering = db.Column(db.Boolean, nullable=True,default=True)
    platenumber = db.Column(db.String(20), db.ForeignKey("car.platenumber"))
    car = relationship("Car", back_populates="detections")
