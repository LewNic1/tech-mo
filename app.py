from flask import Flask, g 
from flask import render_template, flash, redirect, url_for
from flask_login import LoginManager, login_user, login_required, current_user
from flask_bcrypt import check_password_hash

# import json 
import models
import forms 

DEBUG = True
PORT = 8000

app = Flask(__name__) 
app.secret_key = 'molokai'


login_manager = LoginManager() #sets up login
login_manager.init_app(app)
login_manager.login_view = 'login'

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

@app.route('/signup', methods=('GET', 'POST'))
def signup():
    form = forms.SignUpForm()
    if form.validate_on_submit():
        flash('Sign Up Success!')
        models.User.create_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data 
            )
        return redirect(url_for('index'))
    return render_template('signup.html', form=form) 


if __name__ == '__main__':
    models.initialize()

    
    
    
    
    app.run(debug=DEBUG, port=PORT)   