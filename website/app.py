"""
This Flask app contains all of the routes necessary to run digitalpeace.net
"""

from flask import Flask, render_template

from .forms import NewPostSubmissionForm

server = Flask(__name__, static_url_path='/static')
server.config['SECRET_KEY'] = 'my_secret'


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

    new_post = NewPostSubmissionForm()

    #TODO:
    #Add logic to determine user, and post to the appropriate page.
    #If no user is logged in, then it should post the guest page.
    #Limit number of posts by IP. (3 posts should be enough for testing.)

    if new_post.validate_on_submit():
        post_title = new_post.title()
        post_body = new_post.post_body
        post_iamge = new_post.image
        post_image_caption = new_post.image_caption

    return render_template('submit.html', template_form=new_post)


@server.errorhandler(404)
def page_not_found(e):
    return render_template('not_found.html'), 404