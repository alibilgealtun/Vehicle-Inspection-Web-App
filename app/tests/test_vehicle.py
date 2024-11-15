import unittest
from app import create_app, db
from app.models import Vehicle

class VehicleTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_vehicle_crud(self):
        # Create
        vehicle = Vehicle(plate='34XYZ12', brand='Mercedes', model='C200', chassis_number='ABC1234567890', color='BEIGE', model_year=2022, transmission_type='AUTOMATIC', fuel_type='LPG', mileage = 230)
        db.session.add(vehicle)
        db.session.commit()

        # Read
        retrieved_vehicle = Vehicle.query.first()
        self.assertEqual(retrieved_vehicle.plate, '34XYZ12')

        # Update
        retrieved_vehicle.plate = '35ABC34'
        db.session.commit()
        self.assertEqual(retrieved_vehicle.plate, '35ABC34')

        # Delete
        db.session.delete(retrieved_vehicle)
        db.session.commit()
        self.assertEqual(Vehicle.query.count(), 0)

if __name__ == '__main__':
    unittest.main()
