import json
import os
import uuid

from sammy.repositories.user_repository import UserRepository
from sammy.managers.password_manager import PasswordManager

user_repository = UserRepository()


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

    if user_repository.get_item_by_secondary_index(username) is not None:
        return {
            "statusCode": 403,
            "body": json.dumps({
                "message": "User already exists"
            })
        }

    uid = uuid.uuid4()
    hashed_password = PasswordManager.hash_password(password)
    item = {
        'id': uid.hex,
        'username': username,
        'password': hashed_password 
    }
    user_repository.put_item(item)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "id": uid.hex        
        })
    }
