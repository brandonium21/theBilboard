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
        authorize_url='https://login.uber.com/oauth/authorize&scope=profile%20history_lite%20history%20request',
        access_token_url='https://login.uber.com/oauth/token',
        base_url='https://api.uber.com/v1/',
    )

    parameters = {
        'response_type': 'code',
        'redirect_uri': 'https://thebilboard.herokuapp.com/uberDriverAuth2',
        'scope': 'profile',
    }

    # Redirect user here to authorize your application
    login_url = uber_api.get_authorize_url(**parameters)
    return redirect(login_url)


@app.route('/uberDriverAuth2', methods=['GET', 'POST'])
@login_required
def driverAuth2():
    parameters = {'redirect_uri': 'https://thebilboard.herokuapp.com/uberDriverAuth2', 'code': request.args.get('code'), 'grant_type': 'authorization_code', }

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
    



