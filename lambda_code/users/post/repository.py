import boto3

class Repository():
    def __init__(self, table_name):
        client = boto3.resource('dynamodb')
        self.table = client.Table(table_name)

    def get_item(self, key, value):
        dynamo_result = self.table.get_item(
            Key={
                key: value 
            }
        )

        return dynamo_result.get('Item')

    def put_item(self, item):
        self.table.put_item(Item=item)

