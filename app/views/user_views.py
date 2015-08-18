# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>


from flask import redirect, render_template, render_template_string
from flask import request, url_for
from flask_user import current_user, login_required
from app import app, db
from app.models import UserProfileForm
import requests
from rauth import OAuth2Service
import googlemaps
import os
import uuid
from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename

UPLOAD_FOLDER = os.environ['UPLOAD_FOLDER']
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#
# User Profile form
#
@app.route('/user/profile', methods=['GET', 'POST'])
@login_required
def user_profile_page():
    # Initialize form
    form = UserProfileForm(request.form, current_user)

    # Process valid POST
    if request.method == 'POST' and form.validate():

        # Copy form fields to user_profile fields
        form.populate_obj(current_user)

        # Save user_profile
        db.session.commit()

        # Redirect to home page
        return redirect(url_for('home_page'))

    # Process GET or invalid POST
    return render_template('users/user_profile_page.html', form=form)

#
# Uber Driver Auth
#
@app.route('/uberDriverAuth', methods=['GET', 'POST'])
@login_required
def driverAuth():
    uber_api = OAuth2Service(
        client_id='_i56gtxzh6a6Xi-Cn9sTA9HuXuvC41UQ',
        client_secret='C4lOEPSh-RaBgvTH4HS-WLYIPaUy9fR_hNELrYtu',
        name='The Bilboard',
        authorize_url='https://login.uber.com/oauth/authorize',
        access_token_url='https://login.uber.com/oauth/token',
        base_url='https://api.uber.com/v1/',
    )

    parameters = {
        'response_type': 'code',
        'redirect_uri': 'https://thebilboard.herokuapp.com/uberDriverAuth2',
        'scope': 'profile request'
    }

    # Redirect user here to authorize your application
    login_url = uber_api.get_authorize_url(**parameters)
    return redirect(login_url)


@app.route('/uberDriverAuth2', methods=['GET', 'POST'])
@login_required
def driverAuth2():
    parameters = {
        'redirect_uri': 'https://thebilboard.herokuapp.com/uberDriverAuth2',
        'code': request.args.get('code'),
        'grant_type': 'authorization_code',
    }

    response = requests.post(
        'https://login.uber.com/oauth/token',
        auth=(
            '_i56gtxzh6a6Xi-Cn9sTA9HuXuvC41UQ',
            'C4lOEPSh-RaBgvTH4HS-WLYIPaUy9fR_hNELrYtu',
        ),
        data=parameters,
    )

    # This access_token is what we'll use to make requests in the following
    # steps
    access_token = response.json().get('access_token')
    return access_token

@app.route('/createAd', methods=['GET', 'POST'])
def adCreate():
    print 'one'
    if request.method == 'POST':
        print 'two'
        return render_template('pages/createAd.html')
    return render_template('pages/createAd.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/uploaded', methods=['GET', 'POST'])
def upload_file():
    filename = None
    user_id = current_user.id
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = file.filename
            ext = filename.rsplit('.', 1)[1]
            print ext
            filename = secure_filename(file.filename)
            filename = str(uuid.uuid1())
            filename = filename + '.%s' % ext
            #photo_link = "http://" + request.host + "/photos/" + filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #return redirect(url_for('uploaded_file', filename=filename))
            #photo = Photo(0, 0, filename, 'seme', user_id)
            #db.session.commit()
        return filename + ' uploaded successfully'
    return 'you dont belong here'
