import unittest
from app import create_app, db
from app.models import Company

class CompanyTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_company_crud(self):
        # Create
        company = Company(name='Tech Corp', phone_1='1234567890')
        db.session.add(company)
        db.session.commit()

        # Read
        retrieved_company = Company.query.first()
        self.assertEqual(retrieved_company.name, 'Tech Corp')

        # Update
        retrieved_company.name = 'Innovative Corp'
        db.session.commit()
        self.assertEqual(retrieved_company.name, 'Innovative Corp')

        # Delete
        db.session.delete(retrieved_company)
        db.session.commit()
        self.assertEqual(Company.query.count(), 0)

if __name__ == '__main__':
    unittest.main()
