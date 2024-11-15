from datetime import datetime
from ..database import db
from ..enums import ReportStatus


class Report(db.Model):
    __tablename__ = 'report'
    id = db.Column(db.Integer, primary_key=True)
    inspection_date = db.Column(db.DateTime, nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    package_id = db.Column(db.Integer, db.ForeignKey('package.id'), nullable=False)
    operation = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)
    registration_document_seen = db.Column(db.Boolean, nullable=False)
    status = db.Column(db.Enum(ReportStatus), default=ReportStatus.OPENED, nullable=False)

    customer = db.relationship('Customer', back_populates='reports', overlaps="customer_reports,customer")
    package = db.relationship('Package', back_populates='reports')
    staff = db.relationship('Staff', back_populates='reports_created', overlaps="staff_reports,staff")
    vehicle = db.relationship('Vehicle', back_populates='reports')

    def __repr__(self):
        return f'<Report  {self.id}>'
