from flask import Flask, g 
from flask import render_template, flash, redirect, url_for, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import check_password_hash

import models
import os
import forms

DEBUG = True
PORT = 8000

app = Flask(__name__, instance_relative_config=True) 
app.secret_key = 'molokai'

login_manager = LoginManager()
#sets up login
login_manager.init_app(app) 
login_manager.login_view = 'signin'

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
@app.route('/landing')
def landing():
    return render_template('landing.html')
  

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = forms.SignUpForm()
    if form.validate_on_submit():
        flash('Sign up Success!','success')
        models.User.create_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            location=form.location.data
            )
        return redirect(url_for('landing'))
    return render_template('signup.html', title='Sign Up', form=form) 
    

@app.route('/signin', methods=['GET', 'POST'])  
def signin():
    form = forms.SignInForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash('Error. Password or email is incorrect', 'alert alert-danger') 
        else:
            if check_password_hash(user.password, form.password.data): 
                login_user(user) #session created
                flash('Sign in success!', 'success')
                return redirect(url_for('profile'))
            else:
                flash('Error, Password or email is incorrect', 'alert alert-danger')
    return render_template('signin.html', form=form) 


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user = g.user._get_current_object()
    savedresources = models.SavedResources.select(models.Resources).join(models.Resources).where(models.SavedResources.user==user.id)
    print(savedresources)
    for s in savedresources:
        print(s.resource.id)
    return render_template('profile.html', user=g.user._get_current_object(), savedresources=savedresources)
   

@app.route('/edit-profile', methods=['GET', 'POST', 'PUT']) 
@login_required
def edit_profile(): 
    form = forms.EditUserForm()
    
    if form.validate_on_submit():
        mdetails = models.User.select().where(models.User.username==current_user.username).get()
        mdetails.username = form.username.data
        mdetails.email = form.email.data
        mdetails.location = form.location.data
        mdetails.save()
        user = models.User.select().where(models.User.username==form.username.data).get()

        return render_template('profile.html', user=user)
    return render_template('edit-profile.html', form=form, user=current_user)
    

@app.route('/resource', methods=['GET', 'POST'])
@login_required
def resource():
    resources = models.Resources.select().limit(10)

    form = forms.ResourceForm()
    if form.validate_on_submit():
        models.Resources.create(
            user = g.user._get_current_object(),
            category = form.category.data,
            title = form.title.data,
            content = form.content.data
            )
        flash('Resource created!', 'alert alert-success')

        return redirect(url_for ('resource'))

    return render_template('resources.html', form=form, resources=resources)


@app.route('/save/<resource_id>', methods=['GET', 'POST'])
@login_required
def save_to_profile(resource_id=None):
    user = g.user._get_current_object()
    if resource_id != None:
        resource = models.Resources.get(models.Resources.id == resource_id)
        models.SavedResources.create(
            user=user.id,
            resource=resource_id)
        return redirect(url_for('profile'))
    return redirect(url_for('resource'))


@app.route('/delete-resource/<resource_id>', methods=['GET', 'POST'])
@login_required
def delete_resource(resource_id):
    models.Resources.delete_by_id(int (resource_id)) 
    
    return redirect(url_for('resource'))


@app.route('/signout')
@login_required
def signout():
    logout_user()
    flash('Sign out success!', 'alert alert-danger')
    return redirect(url_for('landing'))


if __name__ == '__main__':
    models.initialize()
    try:
        models.User.create_user(
           username = 'Nicolette',
           email = 'Nic@mail.com', 
           password = 'password',
           location = 'Oakland'
        )


        models.Resources.create_resource(
            user = 1,
            category = 'technical',
            title = 'Flask study group',
            content = 'Monday 6pm at GA'
        )
    
    
    
    except ValueError:
        pass 


    app.run(debug=DEBUG, port=PORT)   