import sys
sys.path.append('./layers/SammyService/python/lib/python3.7/site-packages')

import json
from mock import Mock, ANY, patch
import unittest 
import boto3
from boto3.dynamodb.conditions import Key

from sammy.repositories.base_repository import BaseRepository 

@patch('boto3.resource')
class TestUserResource(unittest.TestCase): 

    def mock_tables(self, mocked_resource):
        self.mocked_table = Mock()
        self.mocked_dynamo = Mock()
        self.mocked_dynamo.Table.return_value = self.mocked_table
        mocked_resource.return_value = self.mocked_dynamo

    def test_initiation(self, mocked_resource):
        self.mock_tables(mocked_resource)

        repo = BaseRepository('table_name', 'index')
        repo.table()

        self.mocked_dynamo.Table.assert_called_once_with('table_name')

    def test_get_item(self, mocked_resource):
        self.mock_tables(mocked_resource)
        self.mocked_table.get_item.return_value = {
            'Item': 'item'        
        }

        repo = BaseRepository('table_name', 'index')
        result = repo.get_item('value')

        self.assertEqual(result, 'item')
        self.mocked_table.get_item.assert_called_once_with(
            Key={
                'index': 'value'    
            }
        )

    def test_put_item(self, mocked_resource):
        self.mock_tables(mocked_resource)

        repo = BaseRepository('table_name', 'index')
        repo.put_item('item')

        self.mocked_table.put_item.assert_called_once_with(
            Item='item'
        )

    def test_query_items_by_secondary_index(self, mocked_resource):
        self.mock_tables(mocked_resource)
        self.mocked_table.query.return_value = {
            'Items': ['item']        
        }

        repo = BaseRepository('table_name', 'index', 'secondary_index')
        result = repo.query_by_secondary_index('value')

        self.assertEqual(result[0], 'item')
        self.mocked_table.query.assert_called_once_with(
            IndexName='secondary_index-index',
            KeyConditionExpression=Key('secondary_index').eq('value')
        )
