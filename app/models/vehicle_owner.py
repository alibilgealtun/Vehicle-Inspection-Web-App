from ..database import db

class VehicleOwner(db.Model):
    __tablename__ = 'vehicle_owner'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    tc_tax_number = db.Column(db.String(11), nullable=True, index=True)
    phone_number = db.Column(db.String(15), nullable=False, index=True)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'), nullable=True, index=True)

    address = db.relationship('Address', backref='vehicle_owners', lazy=True)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def __repr__(self):
        return f'<VehicleOwner {self.first_name} {self.last_name}>'
