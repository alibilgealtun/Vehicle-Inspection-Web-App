from ..database import db


class VehicleOwner(db.Model):
    __tablename__ = 'vehicle_owner'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    tc_tax_number = db.Column(db.String(11), nullable=True)
    phone_number = db.Column(db.String(15), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    report_id = db.Column(db.Integer, db.ForeignKey('report.id'), nullable=False)

    def __repr__(self):
        return f'<VehicleOwner {self.full_name}>'