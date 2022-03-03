from sqlalchemy.orm import relationship
from app.models.config import db

class Manufacturer (db.Model):
    __tablename__ = "manufacturer"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    car_types = relationship("CarType", back_populates="manufacturer")