"""
This Flask app contains all of the routes necessary to run digitalpeace.net
"""
from flask import Flask, render_template, redirect
from flask_wtf.csrf import CSRFProtect
from sqlalchemy.sql.expression import desc

from forms import NewPostSubmissionForm
from models import Posts, session
from utils.app_utils.file_handling import no_duplicate_files

server = Flask(__name__, static_url_path='/static')
server.config['SECRET_KEY'] = 'my_secret'
server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///digitalpeaceDB.db'
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

csrf = CSRFProtect(server)


@server.route('/')
def index():
    return render_template('index.html')


@server.route('/austin')
def austin():
    return render_template('austin.html')


@server.route('/adam')
def adam():
    return render_template('adam.html')


@server.route('/guest')
def guest():

    posts = session.query(Posts).all()

    return render_template('guest.html', posts=posts)


@server.route('/post/<int:post_id>')
def post(post_id):
    """
    This route will display all submissions posted by non-members.
    Initially, this will be a posting ground for us.
    Later on, hopefully prospective employers will post here.
    """

    post = session.query(Posts).filter(Posts.id == post_id).first()

    if not post:
        return render_template('not_found.html')

    post_title = post.title
    post_body = post.post_body
    image_file_name = post.image_file_name
    caption = post.image_caption

    # Parsing out new lines from the post body.
    lines = []
    line = ''
    for character in post_body:
        if character != '\n':
            line += character
        else:
            lines.append(line)
            line = ''

    return render_template('post.html',
                           title=post_title,
                           body=lines,
                           image_file_name=image_file_name,
                           caption=caption)


@server.route('/submit', methods=['GET', 'POST'])
def submit_post():

    new_post_submission = NewPostSubmissionForm()

    #TODO:
    #Add logic to determine user, and post to the appropriate page.
    #If no user is logged in, then it should post the guest page.
    #Limit number of posts by IP if not logged in. (3 posts should be enough for posting.)

    #Do stuff with the form data here:
    if new_post_submission.validate_on_submit():
        print("Form submitted!")

        post_title = new_post_submission.title.data
        post_body = new_post_submission.post_body.data
        post_image_caption = new_post_submission.image_caption.data

        post_image_file_name = new_post_submission.image.data.filename
        #Sanitizing input.
        post_image_file_name = post_image_file_name.replace(" ", "")

        # Adding final new line to file.
        post_body += '\n'

        # TODO:
        # Humans separate paragraphs by 2 new lines.
        # Need to convert this to 1 new line after post has been submitted.

        post_image = new_post_submission.image.data

        post_image_file_name = no_duplicate_files(
            post_image_file_name, './static/images/post_images/')

        post_image.save(f'./static/images/post_images/{post_image_file_name}')

        new_post = Posts(title=post_title,
                         post_body=post_body,
                         image_file_name=post_image_file_name,
                         image_caption=post_image_caption)

        try:
            session.add(new_post)
            session.commit()
            print("A new post has been added to db!")

        except Exception as error:
            print(error)
            session.rollback()

        new_post_id = session.query(Posts).order_by(desc(Posts.id)).first().id

        return redirect(f"/post/{new_post_id}")

    else:
        return render_template('submit.html',
                               new_post_submission=new_post_submission)


@server.errorhandler(404)
def page_not_found(e):
    return render_template('not_found.html'), 404


#Example comment for commit