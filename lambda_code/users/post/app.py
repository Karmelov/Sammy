import boto3
import json
import os
import uuid

USERS_TABLE = os.environ['USERS_TABLE_NAME'] 

def lambda_handler(event, context):
    str_body = event['body']
    body = json.loads(str_body)
    
    username = body.get('username')
    if not username:
        return {
            "responseCode": 400,
            "body": json.dumps({
                "message": "'username' field missing"
            })
        }

    password = body.get('password')
    if not password:
        return {
            "responseCode": 400,
            "body": json.dumps({
                "message": "'password' field missing"
            })
        }

    client = boto3.resource('dynamodb')

    table = client.Table(USERS_TABLE)

    uid = uuid.uuid4()
    item = {
        'id': uid.hex,
        'username': username,
        'password': password
    }
    table.put_item(Item=item)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "id": uid.hex        
        })
    }    
