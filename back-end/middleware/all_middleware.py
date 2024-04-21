from flask import abort
from models.Media import MediaAPI
from models.User import User
from models.Comment import Comment


def verify_user(userId):               
    user = User.get_user_by_id_model(userId)
    if not user:
        abort(400, {"message": "User not exist"})
    return user

def verify_email_registered(email):          
    user = User.get_user_by_email_model(email)
    if user:
        abort(400, {"message": "Email is not available"})
    return {"message": "Email is available"}

def verify_username_registered(username):
    user = User.get_user_by_username_model(username)
    if user:
        abort(400, {"message": "Username is not available"})
    return {"message": "Username is available"}




