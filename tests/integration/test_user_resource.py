import unittest
import requests
import os
import json

HOST = os.environ['SAMMY_HOST']

class TestUserResource(unittest.TestCase):
    URL = HOST + 'users'
    
    def test_happy_path(self):
        new_user_data = {
            'username': 'new_user',
            'password': '1234'
        }
        response = requests.post(
            self.URL,
            json=new_user_data
        )
        
        body = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(body['id'])

        uid = body['id']
        
        response = requests.get(
            self.URL + '/' + uid
        )
        body = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(body['username'], 'new_user')
        self.assertEqual(body['password'], '1234')

