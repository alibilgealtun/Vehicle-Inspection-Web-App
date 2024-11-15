import unittest
from app import create_app, db
from app.models import Agent

class AgentTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_agent_crud(self):
        # Create
        agent = Agent(full_name='John Doe', report_id=1)
        db.session.add(agent)
        db.session.commit()

        # Read
        retrieved_agent = Agent.query.first()
        self.assertEqual(retrieved_agent.full_name, 'John Doe')

        # Update
        retrieved_agent.full_name = 'Jane Doe'
        db.session.commit()
        self.assertEqual(retrieved_agent.full_name, 'Jane Doe')

        # Delete
        db.session.delete(retrieved_agent)
        db.session.commit()
        self.assertEqual(Agent.query.count(), 0)

if __name__ == '__main__':
    unittest.main()
