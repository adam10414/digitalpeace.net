"""
This Flask app contains all of the routes necessary to run digitalpeace.net
"""

import os

from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect

from forms import NewPostSubmissionForm
from models import db, Posts
from utils.app_utils.file_handling import no_duplicate_files

server = Flask(__name__, static_url_path='/static')
server.config['SECRET_KEY'] = 'my_secret'
server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///digitalpeaceDB.db'
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

csrf = CSRFProtect(server)

db.init_app(server)


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
        #Sanitizing input.
        post_image_file_name = post_image_file_name.replace(" ", "")

        post_image = new_post_submission.image.data

        post_image_file_name = no_duplicate_files(
            post_image_file_name, './static/images/post_images/')

        post_image.save(f'./static/images/post_images/{post_image_file_name}')

        new_post = Posts(title=post_title,
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