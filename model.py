"""Models for ShowLand app"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_to_db(flask_app, db_uri="postgresql:///showland", echo=False):  # name of the database
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


friend = db.Table(
    'friends',
    db.Column('friend_id', db.Integer, primary_key=True),
    db.Column('f1_id', db.Integer, db.ForeignKey('users.user_id')),
    db.Column('f2_id', db.Integer, db.ForeignKey('users.user_id'))
    )


class User(db.Model):
    """User information"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

    following = db.relationship(
        'User',
        secondary=friend,
        primaryjoin=user_id == friend.c.f1_id,
        secondaryjoin=user_id == friend.c.f2_id,
        backref='followers'
    )


    def get_all_friends(self):
        """ Get all friends, those you are following AND those following you. """
        return self.following + self.followers

    def __repr__(self):
        return f"User user_id = {self.user_id} / email = {self.email}"


class Media(db.Model):
    """Movie's table"""

    __tablename__ = "media"

    media_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    media_type = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    overview = db.Column(db.Text)
    poster_path = db.Column(db.String)
    release_date = db.Column(db.DateTime)
    vote_average = db.Column(db.Float)
    imdb_id = db.Column(db.String, unique=True)
    tmdb_id = db.Column(db.Integer, unique=True)

    def __repr__(self):
        return f"<Media media_id = {self.media_id} / media_type = {self.media_type} / title = {self.title} / imdb_id = {self.imdb_id}"


class Comment(db.Model):

    __tablename__ = "comments"

    comment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comment = db.Column(db.Text, nullable=False)
    review = db.Column(db.Integer)
    media_id = db.Column(db.Integer, db.ForeignKey("media.media_id"))
    user_id = db.Column(db.Integer, db.ForeignKey(
        "users.user_id"), nullable=False)


    media = db.relationship("Media", backref="comments")
    user = db.relationship("User", backref="comments")

    def __repr__(self):
        return f"<Comment comment_id = {self.comment_id} / user_id = {self.user_id}>"


class SaveForLater(db.Model):

    __tablename__ = "later"

    save_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        "users.user_id"), nullable=False)     
    media_id = db.Column(db.Integer, db.ForeignKey("media.media_id"))

    media = db.relationship("Media", backref="savelater")
    user = db.relationship("User", backref="savelater")

    def __repr__(self):
        return f"<SaveForLater save_id = {self.save_id} / user_id = {self.user_id}>"


class Like(db.Model):

    __tablename__ = "likes"

    like_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comment_id = db.Column(db.Integer, db.ForeignKey(
        "comments.comment_id"), nullable=False)  
    user_id = db.Column(db.Integer, db.ForeignKey(
        "users.user_id"), nullable=False)

    comment = db.relationship("Comment", backref="likes")
    user = db.relationship("User", backref="likes")

    def __repr__(self):
        return f"<Like like_id = {self.like_id} / comment_id = {self.comment_id} / user_id = {self.user_id}>"


def example_data():
    """Create some sample data."""

    # In case this is run more than once, empty out existing data
    User.query.delete()


    # Add sample users
    teste2 = User(full_name="teste2", email="teste2@teste.com", password="teste")
    teste3 = User(full_name="teste3", email="teste3@teste.com", password="teste")
    teste5 = User(full_name="teste5", email="teste5@teste.com", password="teste")

    db.session.add_all([teste2, teste3, teste5])
    db.session.commit()



if __name__ == "__main__":
    from server import app

    connect_to_db(app)

    db.create_all()
