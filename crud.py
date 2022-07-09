"""CRUD operations"""
from model import db, User, Media, Comment, SaveForLater, Like, connect_to_db


def create_user(full_name, email, password):
    """Create and return a new user"""

    user = User(full_name=full_name,
                email=email,
                password=password)

    return user


def get_user_by_id(user_id):
    """Return an user by ID."""

    return User.query.filter_by(user_id=user_id).first()

def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter_by(email=email).first()

def create_media(media_type, title, overview, poster_path, imdb_id):
    """Create and return a new media"""

    media = Media(media_type=media_type,title=title, overview=overview, poster_path=poster_path, imdb_id=imdb_id)

    return media

def get_media_by_imdb_id(imdb_id):

    return Media.query.filter_by(imdb_id=imdb_id).first()

# def get_movie_by_imdb_id(imdb_id):

#     return Media.query.filter_by(imdb_id=imdb_id).first()  


# def get_show_by_tmdb_id(tmdb_id):

#     return Media.query.filter_by(tmdb_id=tmdb_id).first()    

def create_comment(comment, review, media_id, user_id,):

    comment = Comment(comment=comment, review=review, media_id=media_id, user_id=user_id)

    return comment

def get_comment_by_id(comment_id):

    comment = Comment.query.filter_by(comment_id=comment_id).first()    
    return comment


def delete_likes_by_comment_id(comment_id):

    likes = Like.query.filter_by(comment_id=comment_id).all()
    for like in likes:
        db.session.delete(like)
    db.session.commit()


def delete_comment_by_id(comment_id):

    comment = Comment.query.get(comment_id)
    if comment.likes:
        delete_likes_by_comment_id(comment_id)
    db.session.delete(comment)
    db.session.commit()

def create_like(user_id, comment_id):

    like = Like(user_id=user_id, comment_id=comment_id) 
    
    return like


def get_like_by_comment_user_id(comment_id, user_id):

    like_by_id = Like.query.filter_by(comment_id=comment_id, user_id=user_id ).first()

    return like_by_id   

def get_like_numbers_by_comment_id(comment_id):

    like = Like.query.filter_by(comment_id=comment_id)
    like_numbers = like.count()

    return like_numbers

def create_save_for_later(user_id, media_id):
    
    save_for_later = SaveForLater(user_id=user_id, media_id=media_id)
    
    return save_for_later

def get_save_for_later_by_media_user_id(user_id, media_id):

    save_later_by_media_usar_id = SaveForLater.query.filter_by(user_id=user_id,media_id=media_id).first()    

    return save_later_by_media_usar_id



if __name__ == "__main__":
    from server import app

    connect_to_db(app)
