import unittest
from app import create_app, db
from app.models import VehicleOwner

class VehicleOwnerTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_vehicleowner_crud(self):
        # Create
        vehicle_owner = VehicleOwner(full_name='Bob Marley', phone_number='5551234567', address='123 Marley Street', report_id=1)
        db.session.add(vehicle_owner)
        db.session.commit()

        # Read
        retrieved_vehicle_owner = VehicleOwner.query.first()
        self.assertEqual(retrieved_vehicle_owner.full_name, 'Bob Marley')

        # Update
        retrieved_vehicle_owner.full_name = 'Robert Marley'
        db.session.commit()
        self.assertEqual(retrieved_vehicle_owner.full_name, 'Robert Marley')

        # Delete
        db.session.delete(retrieved_vehicle_owner)
        db.session.commit()
        self.assertEqual(VehicleOwner.query.count(), 0)

if __name__ == '__main__':
    unittest.main()
