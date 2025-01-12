from ..database import db


    
class Branch(db.Model):
    __tablename__ = 'branch'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'), nullable=True, index=True)

    address = db.relationship('Address', backref='branches', lazy=True)
    company = db.relationship('Company', back_populates='branches')
    staff_members = db.relationship('Staff', back_populates='branch', lazy=True)

    def __repr__(self):
        return f'<Branch {self.name}>'