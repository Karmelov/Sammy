import json

import unittest 

from lambda_code.users.post import app

class TestUserResource(unittest.TestCase):
    def test_lambda_handler(self):

        ret = app.lambda_handler("", "")
        data = json.loads(ret["body"])

        self.assertEqual(data["message"], "postit")

