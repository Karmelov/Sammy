import sys
sys.path.append('./layers/SammyService/python/lib/python3.7/site-packages')

import json
from mock import Mock, ANY, patch
import unittest 
import boto3

from sammy.managers.password_manager import PasswordManager

class TestUserResource(unittest.TestCase): 

    def test_same_password_generates_different_hashes(self):
        hash1 = PasswordManager.hash_password('password')
        hash2 = PasswordManager.hash_password('password')
        
        self.assertNotEqual(hash1, hash2)

    def test_correct_password(self):
        hash1 = PasswordManager.hash_password('password')

        result = PasswordManager.validate_password('password', hash1)

        self.assertTrue(result)
    
    def test_incorrect_password(self):
        hash1 = PasswordManager.hash_password('password')

        result = PasswordManager.validate_password('password2', hash1)

        self.assertFalse(result)
