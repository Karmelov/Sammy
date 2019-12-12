import boto3
import json
import os


USER_TABLE = os.environ['USERS_TABLE_NAME']

def lambda_handler(event, context):
    user_id = event['pathParameters']['id']

    client = boto3.resource('dynamodb')

    table = client.Table(USER_TABLE)

    dynamo_result = table.get_item(
        Key={
            'id': user_id
        }
    )

    user = dynamo_result['Item']

    if user:
        return {
            "statusCode": 200,
            "body": json.dumps(
                user
            ),
        }
    else:
        return {
            "statusCode": 404,
            "body": json.dumps({
                "message": "User not found"
            })
        }
