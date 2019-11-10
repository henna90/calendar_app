import unittest
import server
import os

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
        
        self.assertEqual(result.status_code, 200)


    def test_registration_form(self):
        """Make sure index page returns correct HTML."""

        # Create a test client
        client = server.app.test_client()

        # Use the test client to make requests
        result = client.get('/registration-form')

        # Compare result.data with assert method
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<p> Registartion page </p>', result.data)  

    def test_signup(self):
        """Make sure index page returns correct HTML."""

        # Create a test client
        client = server.app.test_client()

        client_data = {'username': 'henna@gmail.com','password': 'password'}

        # Use the test client to make requests
        result = client.post('/sign-up', data = client_data)

        # Compare result.data with assert method
        self.assertEqual(result.status_code, 400)
          

 
if __name__ == "__main__":
    unittest.main()
    