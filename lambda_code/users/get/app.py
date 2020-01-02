from repository import Repository
import json
import os

USER_TABLE = os.environ['USERS_TABLE_NAME']

users_repository = Repository(USER_TABLE)

def lambda_handler(event, context):
    user_id = event['pathParameters']['id']

    user = users_repository.get_item(key='id', value=user_id)

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
