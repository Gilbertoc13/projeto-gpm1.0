from models.Comment import Comment



def create_comment_controller(username, user_id, content, is_spoiler, media_id):
    comment_id = Comment.create_comment(username, user_id, content, is_spoiler, media_id)
    return comment_id





