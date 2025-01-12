from ..database import db


class Company(db.Model):
    __tablename__ = 'company'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15))
    fax = db.Column(db.String(15))
    email = db.Column(db.String(100))
    website = db.Column(db.String(100))
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'), nullable=True)
    my_business_address_link = db.Column(db.String(255))

    address = db.relationship('Address', backref='companies', lazy=True)
    branches = db.relationship('Branch', back_populates='company', lazy=True)

    def __repr__(self):
        return f'<Company {self.name}>'
