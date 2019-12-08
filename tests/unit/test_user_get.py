import json
import unittest 

from lambda_code.users.get import app

class TestUserResource(unittest.TestCase):
    def test_lambda_handler(self):
        ret = app.lambda_handler("", "")
        data = json.loads(ret["body"])

        self.assertEqual(data["message"], "fake_table_name")

