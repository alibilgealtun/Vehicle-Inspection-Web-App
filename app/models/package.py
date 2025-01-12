from ..database import db



class Package(db.Model):
    __tablename__ = 'package'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    active = db.Column(db.Boolean, default=True)

    reports = db.relationship('Report', back_populates='package', lazy=True)
    package_expertises = db.relationship('PackageExpertise', back_populates='package', cascade="all, delete-orphan", lazy=True)

    def __repr__(self):
        return f'<Package {self.name}>'
    
