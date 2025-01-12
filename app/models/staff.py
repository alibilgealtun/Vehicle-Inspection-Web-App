from ..database import db



class Staff(db.Model):
    __tablename__ = 'staff'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    department = db.Column(db.String(50), nullable=True)
    role = db.Column(db.String(50), nullable=False)

    branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))
    branch = db.relationship('Branch', back_populates='staff_members')

    reports_created = db.relationship('Report', back_populates='staff', lazy=True, overlaps="staff_reports,staff")

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def __repr__(self):
        return f'<Staff {self.first_name} {self.last_name} - {self.role}>'

