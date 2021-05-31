# digitalpeace.net

Welcome to digitalpeace! This is the repo to our website.

## Get Started:
This website uses the Python Flask module. At the time of writing this, we're using Python 3.9.5.

To get started: 
- Clone this repo locally.
- Navigate to the directory locally.
- Run pip install -r requirements.txt

## Running the Flask server locally:
If you don't care about being able to access the site from other devices on the local network, then all you need to do is: 
- Navigate to the directory that contains "app.py". (If you haven't moved anything around, this is in ./website)
- Then run: 
        flask run

If you do care about being able to access the site from other devices, like a mobile device, then run: 
    flask run --host=0.0.0.0

If developer mode is not enabled, then you will need to restart the server every time you make a change to any website file. This is a PITA so, to enable developer mode: 
- First, read this disclaimer by Flask: https://flask.palletsprojects.com/en/2.0.x/server/
- Then run these commands on Mac: 
        $ export FLASK_APP=hello
        $ export FLASK_ENV=development
        $ flask run
        (Remember 'flask run is local use only. If you want this to be viewable on other devices, you'll need to add --host=0.0.0.0')