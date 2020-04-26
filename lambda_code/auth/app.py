import json

from sammy.managers.password_manager import PasswordManager
from sammy.managers.jwt_manager import JwtManager
from sammy.services.users_service import UsersService

users_service = UsersService()

def lambda_handler(event, context):
    str_body = event['body']
    body = json.loads(str_body)

    errors = []
    
    username = body.get('username')
    if not username:
        errors.append("'username' field missing")

    password = body.get('password')
    if not password:
        errors.append("'password' field missing")

    if len(errors) > 0:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": errors
            })
        }

    user = users_service.get_user_by_username(username)
    if user is None:
        return {
            "statusCode": 404,
            "body": json.dumps({
                "message": "User not found"
            })
        }

    is_password_valid = PasswordManager.validate_password(password, user['password'])
    
    if not is_password_valid:
        return {
            "statusCode": 401,
            "body": json.dumps({
                "message": "Invalid credentials"    
            })
        }

    token = JwtManager.create_token(user)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "id": user['id'],
            "token": token
        })
    }

