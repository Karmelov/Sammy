import json
from mock import Mock, ANY, patch
import unittest 
import boto3

from lambda_code.users.get import app

class TestUserResource(unittest.TestCase):
    @patch('boto3.resource')
    def test_lambda_handler(self, mock_dynamo):
        mock_table = Mock()
        mock_dynamo.return_value.Table.return_value = mock_table
        mock_table.get_item.return_value = {
            "Item": {
                "user": "data"    
            }        
        }

        event = dict()
        event['pathParameters'] = {
            'id': 'unique_uuid'
        }

        ret = app.lambda_handler(event, "")
        data = json.loads(ret["body"])

        mock_table.get_item.assert_called_once_with(
                Key={
                    'id': 'unique_uuid'
                }
        )
        self.assertEqual(data['user'], 'data')

