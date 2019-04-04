from flask import Flask, g, request
from flask import render_template, flash, redirect, url_for, session, escape 
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from flask_bcrypt import check_password_hash
from werkzeug.urls import url_parse 

# import json 
import models
import forms 
import os 

DEBUG = True
PORT = 8000

app = Flask(__name__, instance_relative_config=True) 
# app.config.from_pyfile('flask.ctg')
app.secret_key = 'molokai'


login_manager = LoginManager() #sets up login
login_manager.init_app(app)
login_manager.login_view = 'login'

# images = UploadSet('imges', IMAGES)
# configure_uploads(app, images)

@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None 


@app.before_request
def before_request():
    g.db = models.DATABASE   #CONNECTS TO DB BEFORE EACH REQUEST
    g.db.connect()
    g.user = current_user 

@app.after_request
def after_request(response):   #CLOSES THE DB AFTER EACH REQUEST
    g.db.close()
    return response 



@app.route('/')
def index():
    return render_template('landing.html')  

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = forms.SignUpForm()
    if form.validate_on_submit():
        # filename = images.save(request.files['profile_image'])
        # url = images.url(filename)
       
        models.User.create_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data, 
            location=form.location.data)
            # image_filename=filename,
            # image_url=url
            
        user = models.User.get(models.User.username == form.username.data)
        login_user(user)
        name = user.username
        flash('Sign Up Success!') 
        return redirect(url_for('profile', username=name))
    return render_template('signup.html', form=form) 

@app.route('/signin', methods=['GET', 'POST'])  
def signin():
    form = forms.SignInForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash("Error", "Password or email is incorrect") 
        else:
            if check_password_hash(user.password, form.password.data): 
                login_user(user) #session created
                flash("sign in success!")
                return redirect(url_for('profile', username=user.username))
            else:
                flash("Error", "Passeord or email is incorrect")
    return render_template('signin.html', form=form) 

@app.route('/signout')
@login_required
def signout():
    signout_user()
    flash("Sign out success!")
    return redirect(url_for('index'))


if __name__ == '__main__':
    models.initialize()

    
    
    
    
    app.run(debug=DEBUG, port=PORT)   