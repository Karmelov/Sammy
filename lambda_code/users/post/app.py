import json
import os
import uuid

from sammy.services.users_service import UsersService

users_service = UsersService()


def lambda_handler(event, context):
    str_body = event['body']
    body = json.loads(str_body)
    
    username = body.get('username')
    if not username:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "'username' field missing"
            })
        }

    password = body.get('password')
    if not password:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "'password' field missing"
            })
        }

    try:
        user = users_service.create_user(username, password)
    except ValueError as ex:
        return {
            "statusCode": 403,
            "body": json.dumps({
                "message": "User already exists"
            })
        }

    return {
        "statusCode": 200,
        "body": json.dumps({
            "id": user['id']        
        })
    }
