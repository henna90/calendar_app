import unittest

import server

class TestFlaskRoutes(unittest.TestCase):
    """Test Flask routes."""

    def setUp(self):
        """Completed before each test"""

        self.client = server.app.test_client()
        server.app.config['TESTING'] = True

    def test_index(self):
        """Make sure index page returns correct HTML."""

        # Create a test client
        client = server.app.test_client()

        # Use the test client to make requests
        result = client.get('/')

        # Compare result.data with assert method
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<h1> Welcome to my Calendar </h1>', result.data)



    