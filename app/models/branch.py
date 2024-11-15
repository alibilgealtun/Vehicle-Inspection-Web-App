from ..database import db


class Branch(db.Model):
    __tablename__ = 'branch'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # Branch name or identifier
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    address = db.Column(db.String(255))
    phone_1 = db.Column(db.String(15))
    phone_2 = db.Column(db.String(15))
    fax = db.Column(db.String(15))
    email = db.Column(db.String(100))
    staff_members = db.relationship('Staff', backref='branch', lazy=True)

    def __repr__(self):
        return f'<Branch {self.name} - {self.company.name}>'