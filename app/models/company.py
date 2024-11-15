from ..database import db


class Company(db.Model):
    __tablename__ = 'company'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone_1 = db.Column(db.String(15))
    phone_2 = db.Column(db.String(15))
    fax = db.Column(db.String(15))
    email = db.Column(db.String(100))
    website = db.Column(db.String(100))
    address = db.Column(db.String(255))
    my_business_address_link = db.Column(db.String(255))
    branches = db.relationship('Branch', backref='company', lazy=True)

    def __repr__(self):
        return f'<Company {self.name}>'
