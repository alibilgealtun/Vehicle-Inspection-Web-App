import unittest
from app import create_app, db
from app.models import Package

class PackageTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_package_crud(self):
        # Create
        package = Package(name='Basic Package', price=100.0, contents='Expertise 1, Expertise 2')
        db.session.add(package)
        db.session.commit()

        # Read
        retrieved_package = Package.query.first()
        self.assertEqual(retrieved_package.name, 'Basic Package')

        # Update
        retrieved_package.name = 'Premium Package'
        db.session.commit()
        self.assertEqual(retrieved_package.name, 'Premium Package')

        # Delete
        db.session.delete(retrieved_package)
        db.session.commit()
        self.assertEqual(Package.query.count(), 0)

if __name__ == '__main__':
    unittest.main()
