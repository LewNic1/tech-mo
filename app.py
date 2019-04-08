from flask import Flask, g 
from flask import render_template, flash, redirect, url_for, request
# from forms import SignUpForm, SignInForm, EditUserForm, ResourceForm, EditResourceForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import check_password_hash

# from flask import session, escape, request
# from werkzeug.urls import url_parse #redirect user if not signed in

import models
import os
import forms
# import flask_user
 

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
        flash('Sign up Success!', 'success')
        models.User.create_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            location='San Francisco'
            )
        return redirect(url_for('profile'))
    return render_template('signup.html', title='Sign Up', form=form) 
    

@app.route('/signin', methods=['GET', 'POST'])  
def signin():
    form = forms.SignInForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash('Error. Password or email is incorrect', 'danger') 
        else:
            if check_password_hash(user.password, form.password.data): 
                login_user(user) #session created
                flash('Sign in success!', 'success')
                return redirect(url_for('profile'))
            else:
                flash('Error, Password or email is incorrect', 'danger')
    return render_template('signin.html', form=form) 

@app.route('/profile', methods=['GET', 'POST', 'PUT'])
@login_required
def profile():
    form = forms.EditUserForm()
    
    if form.validate_on_submit():
        mdetails = models.User.select().where(models.User.username==current_user.username).get()
        mdetails.username = form.username.data
        mdetails.email = form.email.data
        mdetails.location = form.location.data
        mdetails.save()
        user = models.User.select().where(models.User.username==form.username.data).get()

        return render_template('edit-profile.html', form=form, user=user)
    return render_template('edit-profile.html', form=form, user=current_user)
    # user = models.User.select().where(models.User.username==username).get()
    # resources = models.Resources.select().where(models.Resources.user == user.id).order_by(-models.Resources.timestamp)

        # Owner = user.alias()
        # Saved_resources = models.SavedResources.select(models.SavedResources, models.Resources.title, models.Resources.id, models.User.username) #Owner.username)
        # .join(Owner)
        # .switch(models.SavedResources)
        # .join(models.Resources)
        # .join(models.User)

    
    # return redirect(url_for('landing')) 

# #==============
# # Create Resource route
# # =============
# @app.route('/create-resource', methods=['GET', 'POST'])
# @login_required
# def add_resource():
#     form = forms.ResourceForm()
#     user = g.user._get_current_object()

#     models.Resource.create(
#         category = form.category.data,
#         title = form.title.data,
#         content = form.content.data
#         user = g.user._get_current_object()
#         resource = models.Resource.get(models.Resource.title == form.title.data) 
#     flash('Success!' 'Resource created!')
#     return redirect(url_for ('resource', resource_id=resource.id))   
# else:
#     retuen render_template('create-resource.html', form=form, user=user) 

 
# @app.route('/resources', methods=['GET','PUT'])
# @app.route('/resources/,resource_id>', methods=['GET', 'PUT'])
# @login_required
# def resources(resource_id=None):
#     if resource_id !=None and request.method =='GET':
#         resource = models.Resource.select().where(models.Resource.id == resource_id).get()
#         return render_template('resource.html', resource=resource)
#     resources = models.Resource.select().limit(10)
#     return render_template('resources.html', resources=resources) 



@app.route('/signout')
# @login_required
def signout():
    # signout_user()
    flash("Sign out success!")
    return redirect(url_for('landing'))


if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)   