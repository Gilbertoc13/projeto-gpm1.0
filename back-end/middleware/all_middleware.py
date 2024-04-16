from flask import abort
from models.Midia import Midia
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

def verify_movie(movie_id):
    verify_movie(movie_id)
    movie = Midia.get_movie_by_id_model(movie_id)
    previous_movie = movie.get("previousMovieId")
    if previous_movie:
        return previous_movie
    return False

def verify_comment(comment_id):
    verify_comment(comment_id)
    comment = Comment.get_comment_by_id(comment_id)
    previous_comment = Comment.get("previousCommentId")
    if previous_comment:
        return previous_comment
    return False




