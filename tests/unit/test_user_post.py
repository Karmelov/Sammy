import json
from mock import Mock, ANY, patch
import unittest 
import boto3

from lambda_code.users.post import app

class TestUserResource(unittest.TestCase):
    @patch('boto3.resource')
    def test_lambda_handler(self, mock_dynamo):
        mock_table = Mock()
        mock_dynamo.return_value.Table.return_value = mock_table

        event = dict()
        event['body'] = json.dumps({
            'username': 'test_username',
            'password': 'test_password'
        })
        ret = app.lambda_handler(event, "")
        data = json.loads(ret["body"])

        mock_table.put_item.assert_called_once_with(
                Item={
                    'id': ANY,
                    'username': 'test_username',
                    'password': 'test_password'
                }
        )

