import unittest
from app import create_app, db
from app.models import Staff

class StaffTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_staff_crud(self):
        # Create
        staff = Staff(full_name='Charlie Brown', password='password123', phone_number='5557654321', department='Sales', role='Manager', branch_id=1)
        db.session.add(staff)
        db.session.commit()

        # Read
        retrieved_staff = Staff.query.first()
        self.assertEqual(retrieved_staff.full_name, 'Charlie Brown')

        # Update
        retrieved_staff.full_name = 'Charles Brown'
        db.session.commit()
        self.assertEqual(retrieved_staff.full_name, 'Charles Brown')

        # Delete
        db.session.delete(retrieved_staff)
        db.session.commit()
        self.assertEqual(Staff.query.count(), 0)

if __name__ == '__main__':
    unittest.main()
