from app.models.config import db
from sqlalchemy.orm import relationship 
from flask_login import UserMixin
import enum

class Role(enum.Enum):
    admin = 1
    other = 2

class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    eduid = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    role = db.Column(db.Enum(Role), default=Role.other)
    cars = relationship("Car", back_populates="user")

    @property
    def fullname(self):
        return self.firstname + " " + self.lastname
