from datetime import datetime
from sqlalchemy.orm import validates
from ..database import db
from ..enums import TransmissionType, FuelType, Color


from sqlalchemy.orm import validates


class Vehicle(db.Model):
    __tablename__ = 'vehicle'
    id = db.Column(db.Integer, primary_key=True)
    plate = db.Column(db.String(10), nullable=False, unique=True)
    engine_number = db.Column(db.String(17), nullable=True, unique=True)
    brand = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    chassis_number = db.Column(db.String(17), nullable=False, unique=True)
    color = db.Column(db.Enum(Color), nullable=False)
    model_year = db.Column(db.Integer, nullable=False)
    transmission_type = db.Column(db.Enum(TransmissionType), nullable=False)
    fuel_type = db.Column(db.Enum(FuelType), nullable=False)
    mileage = db.Column(db.Integer, nullable=False)

    reports = db.relationship('Report', back_populates='vehicle', lazy=True)

    @validates('model_year')
    def validate_model_year(self, key, value):
        current_year = datetime.now().year
        if value < 1950 or value > current_year:
            raise ValueError(f'Model year must be between 1950 and {current_year}.')
        return value

    def __repr__(self):
        return f'<Vehicle {self.plate} - {self.brand} {self.model}>'