import unittest
from app import create_app, db
from app.models import Customer

class CustomerTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_customer_crud(self):
        # Create
        customer = Customer(full_name='Alice Smith', phone_number='9876543210')
        db.session.add(customer)
        db.session.commit()

        # Read
        retrieved_customer = Customer.query.first()
        self.assertEqual(retrieved_customer.full_name, 'Alice Smith')

        # Update
        retrieved_customer.full_name = 'Alice Johnson'
        db.session.commit()
        self.assertEqual(retrieved_customer.full_name, 'Alice Johnson')

        # Delete
        db.session.delete(retrieved_customer)
        db.session.commit()
        self.assertEqual(Customer.query.count(), 0)

if __name__ == '__main__':
    unittest.main()
