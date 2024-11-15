import unittest
from app import create_app, db
from app.models import Branch

class BranchTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_branch_crud(self):
        # Create
        branch = Branch(name='Main Branch', company_id=1, address='123 Main St')
        db.session.add(branch)
        db.session.commit()

        # Read
        retrieved_branch = Branch.query.first()
        self.assertEqual(retrieved_branch.name, 'Main Branch')

        # Update
        retrieved_branch.name = 'Secondary Branch'
        db.session.commit()
        self.assertEqual(retrieved_branch.name, 'Secondary Branch')

        # Delete
        db.session.delete(retrieved_branch)
        db.session.commit()
        self.assertEqual(Branch.query.count(), 0)

if __name__ == '__main__':
    unittest.main()
