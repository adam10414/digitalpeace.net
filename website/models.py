from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Users(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(), index=True)

    #posts = db.relationship('Post', backref=db.backref('posts', lazy=True))


class Posts(Base):

    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(String(20), index=True, nullable=False)
    post_body = Column(String(), index=False, nullable=False)
    image_file_name = Column(String(), index=True, nullable=False)
    image_caption = Column(String(50), index=True, nullable=False)

    #user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f""""       Post title: {self.title}
        Post Body: {self.post_body}
        Image File Name: {self.image_file_name}
        Image Caption: {self.image_caption}"""


# Connection
engine = create_engine('sqlite:///digitalpeaceDB.db')

# Create metadata
Base.metadata.create_all(engine)

# create session
Session = sessionmaker(bind=engine)
session = Session()

# Testing...
test = session.query(Posts).first()

print(test)

#db.create_all()