from sammy.repositories.user_repository import UserRepository
import json
import os


user_repository = UserRepository()

def lambda_handler(event, context):
    user_id = event['pathParameters']['id']

    user = user_repository.get_item(user_id)

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
