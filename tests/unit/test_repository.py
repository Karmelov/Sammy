import sys
sys.path.append('./layers/repositories/python/lib/python3.7/site-packages')

import json
from mock import Mock, ANY, patch
import unittest 
import boto3

from repository import Repository 

@patch('boto3.resource')
class TestUserResource(unittest.TestCase): 

    def mock_tables(self, mocked_resource):
        self.mocked_table = Mock()
        self.mocked_dynamo = Mock()
        self.mocked_dynamo.Table.return_value = self.mocked_table
        mocked_resource.return_value = self.mocked_dynamo

    def test_initiation(self, mocked_resource):
        self.mock_tables(mocked_resource)

        repo = Repository('table_name')
        repo.table()

        self.mocked_dynamo.Table.assert_called_once_with('table_name')

    def test_get_item(self, mocked_resource):
        self.mock_tables(mocked_resource)
        self.mocked_table.get_item.return_value = {
            'Item': 'item'        
        }

        repo = Repository('table_name')
        result = repo.get_item('key', 'value')

        self.assertEqual(result, 'item')
        self.mocked_table.get_item.assert_called_once_with(
            Key={
                'key': 'value'    
            }
        )

    def test_put_item(self, mocked_resource):
        self.mock_tables(mocked_resource)

        repo = Repository('table_name')
        repo.put_item('item')

        self.mocked_table.put_item.assert_called_once_with(
            Item='item'
        )

