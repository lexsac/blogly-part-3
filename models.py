"""Models for Blogly."""
import datetime
from flask_sqlalchemy import SQLAlchemy

# initialize variable, run SQLAlchemy and store in this variable
db = SQLAlchemy()

#associate Flask app with this db variable
def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """User."""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    first_name = db.Column(db.String, 
                    nullable=False)

    last_name = db.Column(db.String, 
                    nullable=False)

    image_url = db.Column(db.Text, default="https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png")

    posts = db.relationship("Post", backref="user")


class Post(db.Model):
    """Post."""

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    title = db.Column(db.Text, 
                    nullable=False)

    content = db.Column(db.Text, 
                    nullable=False)

    created_at = db.Column(db.DateTime,
                    nullable=False,
                    default=datetime.datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class Tag(db.Model): 
    """Tag."""

    __tablename__ = "tags"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    name = db.Column(db.Text, 
                    unique=True)

    posts = db.relationship('Post', secondary="posts_tags", backref="tags")


class PostTag(db.Model): 

    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, db.ForeignKey(
        'posts.id'), primary_key=True, nullable=False)

    tag_id = db.Column(db.Integer, db.ForeignKey(
        'tags.id'), primary_key=True, nullable=False)