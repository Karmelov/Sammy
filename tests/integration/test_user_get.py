import unittest
import requests
import os

HOST = os.environ['SAMMY_HOST']

class TestUserResource(unittest.TestCase):
    URL = HOST + '/users'
    
    def test_endpoint(self):
        response = requests.get(self.URL)
        
        body = response.json()
        self.assertEqual(body['message'], "UsersTable")

