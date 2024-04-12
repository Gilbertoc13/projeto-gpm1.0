from models.Comment import Comment
from bson import ObjectId


def create_comment_controller(username, user_id, content, is_spoiler, media_id):
    comment_id = Comment.create_comment_evaluation_model(username, user_id, content, is_spoiler, media_id)
    return comment_id


