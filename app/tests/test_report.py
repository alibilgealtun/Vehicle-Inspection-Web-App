import unittest
from datetime import datetime
from app import create_app, db
from app.models import Report

class ReportTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_report_crud(self):
        # Create
        report = Report(inspection_date=datetime(2024, 1, 2), vehicle_id=1, customer_id=1, package_id=1, created_by=1, registration_document_seen=True)
        db.session.add(report)
        db.session.commit()

        # Read
        retrieved_report = Report.query.first()
        self.assertEqual(retrieved_report.vehicle_id, 1)

        # Update
        retrieved_report.vehicle_id = 2
        db.session.commit()
        self.assertEqual(retrieved_report.vehicle_id, 2)

        # Delete
        db.session.delete(retrieved_report)
        db.session.commit()
        self.assertEqual(Report.query.count(), 0)

if __name__ == '__main__':
    unittest.main()
