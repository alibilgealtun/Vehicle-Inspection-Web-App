from ..database import db

class Customer(db.Model):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    tc_tax_number = db.Column(db.String(11), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'), nullable=True)

    address = db.relationship('Address', backref='customers', lazy=True)
    reports = db.relationship('Report', back_populates='customer', lazy=True, overlaps="customer_reports,customer")

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def __repr__(self):
        return f'<Customer {self.first_name} {self.last_name}>'