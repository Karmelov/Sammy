import unittest
import requests
import os
import json

from random import random

HOST = os.environ['SAMMY_HOST']

class TestUserResource(unittest.TestCase):
    URL = HOST + 'users'

    def setUp(self):
        self.username = 'user' + str(random())

    def test_happy_path(self):
        new_user_data = {
            'username': self.username,
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
        self.assertEqual(body['username'], self.username)

    def test_user_already_exists(self):

        new_user_data = {
            'username': self.username,
            'password': '1234'
        }
        response = requests.post(
            self.URL,
            json=new_user_data
        )
        
        body = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(body['id'])

        response = requests.post(
            self.URL,
            json=new_user_data
        )
        
        body = response.json()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(body['message'], 'User already exists')

