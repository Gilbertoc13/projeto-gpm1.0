from models.Comment import Comment
from middleware.all_middleware import verify_comment



def create_comment_controller(username, user_id, content, is_spoiler, media_id):
    comment_id = Comment.create_comment_evaluation_model(username, user_id, content, is_spoiler, media_id)
    return comment_id


def update_comment(comment_id, updated_fields):
    try:
        return Comment.update_comment(comment_id, updated_fields)
    except Exception as e:
        print(f"Error updating comment: {e}")
        return False

def delete_comment(comment_id):
    try:
        return Comment.delete_comment(comment_id)
    except Exception as e:
        print(f"Error deleting comment: {e}")
        return False

def list_comments(media_id):
    try:
        return Comment.get_comment_by_id(media_id)
    except Exception as e:
        print(f"Error listing comments: {e}")
        return []



