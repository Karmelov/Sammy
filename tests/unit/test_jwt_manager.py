import sys
sys.path.append('./layers/SammyService/python/lib/python3.7/site-packages')

import json
from mock import Mock, ANY, patch
import unittest 
import boto3
from freezegun import freeze_time

mock_secret_manager = Mock()
boto3.client = Mock()
boto3.client.return_value = mock_secret_manager
mock_secret_manager.get_secret_value.return_value = {"SecretString": "FakeSecret"}

from sammy.managers.jwt_manager import JwtManager

class TestUserResource(unittest.TestCase): 

    def test_token_decode(self):
        token = JwtManager.create_token('payload')
        payload = JwtManager.decode_token(token)

        self.assertEqual(payload, 'payload')
    
    def test_expired_token(self):
        with freeze_time("2020-01-01 13:00:00"):
            token = JwtManager.create_token('payload')
        with freeze_time("2020-01-01 13:16:00"): 
            self.assertRaises(ValueError, JwtManager.decode_token, token)

