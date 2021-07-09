"""
This Flask app contains all of the routes necessary to run digitalpeace.net
"""

import os

from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String

from .forms import NewPostSubmissionForm

server = Flask(__name__, static_url_path='/static')
server.config['SECRET_KEY'] = 'my_secret'
server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///digitalpeaceDB.db'
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

csrf = CSRFProtect(server)

db = SQLAlchemy(server)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), index=True)

    #posts = db.relationship('Post', backref=db.backref('posts', lazy=True))


class Post(db.Model):
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


@server.route('/')
def index():
    return render_template('index.html')


@server.route('/austin')
def austin():
    return render_template('austin.html')


@server.route('/adam')
def adam():
    return render_template('adam.html')


#TODO:
#Add a guest page for randos on the internet to post to. (Low priority)


@server.route('/submit', methods=['GET', 'POST'])
def submit_post():

    new_post_submission = NewPostSubmissionForm()

    #TODO:
    #Add logic to determine user, and post to the appropriate page.
    #If no user is logged in, then it should post the guest page.
    #Limit number of posts by IP if not logged in. (3 posts should be enough for testing.)

    #Do stuff with the form data here:
    if new_post_submission.validate_on_submit():
        print("Form submitted!")

        post_title = new_post_submission.title.data
        post_body = new_post_submission.post_body.data
        post_image_caption = new_post_submission.image_caption.data

        post_image_file_name = new_post_submission.image.data.filename
        post_image = new_post_submission.image.data

        #TODO:
        #Find a faster way of doing this.

        #Checking to see if the file name exists already, and if so, append a number to the end of the filename.
        counter = 2
        while os.path.exists(
                f'./static/images/post_images/{post_image_file_name}'):

            #Temporarily removing the file extension, and inserting the counter.
            file_extension = post_image_file_name[post_image_file_name.find('.'
                                                                            ):]
            post_image_file_name = post_image_file_name[:post_image_file_name.
                                                        find('.')]

            post_image_file_name += str(counter)
            counter += 1

            #Adding the file extension back to the image.
            post_image_file_name += file_extension

            #TODO:
            #Currently this counter will append numbers to the end of the file name like this:
            #test.jpg
            #test2.jpg
            #test23.jpg
            #test.234.jpg
            #etc...

            #While totally unimportant, but a nice to have:
            #Find a way to increment the filename by 1, rather than just appending a number to the end of the filename.

        post_image.save(f'./static/images/post_images/{post_image_file_name}')

        new_post = Post(title=post_title,
                        post_body=post_body,
                        image_file_name=post_image_file_name,
                        image_caption=post_image_caption)

        try:
            db.session.add(new_post)
            db.session.commit()
            print("Stuff added to db!")

        except Exception as error:
            print(error)
            db.session.rollback()

        return render_template('submit.html',
                               new_post_submission=new_post_submission,
                               post_title=post_title,
                               post_body=post_body,
                               post_image=post_image,
                               post_image_caption=post_image_caption,
                               post_image_file_name=post_image_file_name)

    else:
        return render_template('submit.html',
                               new_post_submission=new_post_submission)


@server.errorhandler(404)
def page_not_found(e):
    return render_template('not_found.html'), 404


#Example comment for commit