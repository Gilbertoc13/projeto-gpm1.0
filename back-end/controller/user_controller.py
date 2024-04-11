import bcrypt
import base64
from flask_jwt_extended import create_access_token
from models.User import User

def login(email, password):
    user = User.get_user_by_email_model(email)
    if user and bcrypt.checkpw(password.encode(), base64.b64decode(user["password"].encode())):
        token = create_access_token(identity=email)
        return {"access_token": token}, 200
    if not user:
        return {"message": "User not in database"}, 402
    else:
        return {"message": "Invalid username or password"}, 401

def create_user_controller(email, username, password):
    existing_user = User.get_user_by_username_model(email)  
    if existing_user:
        return {"message": "Username already exists"}, 400

    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    hashed_password_base64 = base64.b64encode(hashed_password).decode()
    user_id = User.create_user_model(email, username, hashed_password_base64)
    token = create_access_token(identity=email)
    return {"id": user_id, "message": f"User {username} created", "access_token": token}, 201

