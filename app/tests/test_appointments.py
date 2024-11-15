import unittest
from app import create_app, db
from app.models import Appointment
from datetime import datetime, time


class AppointmentTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_appointment_crud(self):
        # Create
        appointment = Appointment(customer_id=1, date=datetime(2024, 1, 1), time=time(10, 0, 0), brand='BMW', model='X5')
        db.session.add(appointment)
        db.session.commit()

        # Read
        retrieved_appointment = Appointment.query.first()
        self.assertEqual(retrieved_appointment.brand, 'BMW')

        # Update
        retrieved_appointment.brand = 'Audi'
        db.session.commit()
        self.assertEqual(retrieved_appointment.brand, 'Audi')

        # Delete
        db.session.delete(retrieved_appointment)
        db.session.commit()
        self.assertEqual(Appointment.query.count(), 0)

if __name__ == '__main__':
    unittest.main()
