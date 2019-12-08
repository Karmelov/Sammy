import boto3
import json
import os


USER_TABLE = os.environ['USERS_TABLE_NAME']

def lambda_handler(event, context):

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": USER_TABLE,
        }),
    }
