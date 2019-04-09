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
        # user = models.User.get(models.User.id == userid)
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
            location=form.location.data
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

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
   
    return render_template('profile.html', user=g.user._get_current_object())
    
    
    
    
    
    
    

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
    

@app.route('/resource', methods=['GET'])
@app.route('/resource/<resource_id>', methods=['GET', 'PUT']) 
@login_required
def resource(resource_id=None):
    if resource_id !=None and request.method =='GET':
        resource = models.Resource.select().where(models.Resource.id == resource_id).get()
        return render_template('resource.html', resource=resource)
    resources = models.Resources.select().limit(10)
    return render_template('resources.html', resources=resources)



@app.route('/create-resource', methods=['GET', 'POST'])
@login_required
def add_resource():
    form = forms.ResourceForm()
    user = g.user._get_current_object()

    if form.validate_on_submit():
        models.Resource.create(
            category = form.category.data,
            title = form.title.data,
            content = form.content.data,
            user = g.user._get_current_object())
    
        resource = models.Resource.get(models.Resource.title == form.title.data) 
        flash('Resource created!', 'Success!')
        return redirect(url_for ('resource', resource_id=resource.id))   
    else:
        return render_template('create-resource.html', form=form, user=user) 

 
@app.route('/edit-resource/<resource_id>', methods=['GET', 'POST', 'PUT']) 
@login_required
def edit_resource():
    form = forms.EditResourceForm()
    
    if form.validate_on_submit():
        mdetails = models.User.select().where(models.User.username==current_user.username).get()
        mdetails.category = form.category.data
        mdetails.title = form.title.data
        mdetails.content = form.content.data
        mdetails.save()
        user = models.User.select().where(models.User.username==form.username.data).get()

        return render_template('edit-resource.html', form=form, user=user)
    return render_template('resource.html', form=form, user=current_user)

@app.route('/save/<resource_id>')
@login_required
def save_to_profile(resource_id=None):
    if resource_id != None:
        user = g.user._get_current_object()
        resource = models.Resource.get(models.Resource.id == resource_id) 

        models.SavedResources.create(user=user.id, resource=resource.id)
        return redirect(url_for('profile', username=user.username))
    return redirect(url_for('resource'))

@app.route('/delete-resource/<resource_id>', methods=['GET','DELETE'])
@login_required
def delete_resource(resource_id=None):
    if resource_id != None:
        deleted_saved_resource = models.SavedResources.delete().where(models.SavedResources.resource == resource_id)
        deleted_saved_resource.excute()

        deleted_resource = models.Resource.delete().where(models.Resource.id == resource_id)
        deleted_resource.excute()

        return redirect(url_for('resource'))
    return redirect(url_for('resource', resource_id))


@app.route('/signout')
@login_required
def signout():
    logout_user()
    flash("Sign out success!")
    return redirect(url_for('landing'))


if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)   