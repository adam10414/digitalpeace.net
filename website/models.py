from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String

db = SQLAlchemy()


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), index=True)

    #posts = db.relationship('Post', backref=db.backref('posts', lazy=True))


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), index=True, nullable=False)
    post_body = db.Column(db.String(), index=False, nullable=False)
    image_file_name = db.Column(db.String(), index=True, nullable=False)
    image_caption = db.Column(db.String(50), index=True, nullable=False)

    #user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    __repr__ = f""""Post title: {title}
    Post Body: {post_body}
    Image File Name: {image_file_name}
    Image Caption: {image_caption}"""


#db.create_all()