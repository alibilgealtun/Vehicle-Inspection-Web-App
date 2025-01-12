from ..database import db

class Appointment(db.Model):
    __tablename__ = 'appointment'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False, index=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    brand = db.Column(db.String(50), nullable=True)
    model = db.Column(db.String(50), nullable=True)
    reminder_sent = db.Column(db.Boolean, default=False)

    customer = db.relationship('Customer', backref='appointments', lazy=True)

    def __repr__(self):
        return f'<Appointment {self.brand} - {self.date} {self.time}>'
