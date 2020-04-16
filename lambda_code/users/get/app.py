from sammy.services.users_service import UsersService
import json
import os


users_service = UsersService()

def lambda_handler(event, context):
    user_id = event['pathParameters']['id']

    user = users_service.get_user_by_id(user_id)

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
