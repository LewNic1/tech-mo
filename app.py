from flask import Flask, g, request
from flask import render_template, flash, redirect, url_for, session, escape 
from flask_bcrypt import check_password_hash
from werkzeug.urls import url_parse #redirect user if not signed in
# from forms import SignUpForm, SignInForm, EditUserForm, ResourceForm, EditResourceForm
 
import models
# import forms 
import os 

DEBUG = True
PORT = 8000

app = Flask(__name__, instance_relative_config=True) 

app.secret_key = 'molokai'

@app.before_request
def before_request():
    g.db = models.DATABASE   #CONNECTS TO DB BEFORE EACH REQUEST
    g.db.connect()
    # g.user = current_user 

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
    form = SignUpForm()
    if form.validate_on_submit():
        flash('Sign up Success!', 'success')
        return redirect(url_for('profile', username=name))
    return render_template('signup.html', title='Sign Up', form=form) 
    

@app.route('/signin', methods=['GET', 'POST'])  
def signin():
    form = SignInForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash('Error. Password or email is incorrect', 'danger') 
        else:
            if check_password_hash(user.password, form.password.data): 
                login_user(user) #session created
                flash('Sign in success!', 'success')
                return redirect(url_for('profile', username=user.username))
            else:
                flash('Error, Password or email is incorrect', 'danger')
    return render_template('signin.html', form=form) 

@app.route('/profile/<username>', methods=['GET'])
# @login_required
def profile(username=None):
    if username != None and request.method == 'GET':
        user = models.User.select().where(models.User.username==username).get()
        # resources = models.Resources.select().where(models.Resources.user == user.id).order_by(-models.Resources.timestamp)

    #     Owner = user.alias()
    #     Saved_resources = models.SavedResources.select(models.SavedResources, models.Resources.title, models.Resources.id, models.User.username) #Owner.username)
    #     .join(Owner)
    #     .switch(models.SavedResources)
    #     .join(models.Resources)
    #     .join(models.User)

        return render_template('profile.html', user=user)
   
    return redirect(url_for('index')) 

@app.route('/edit-profile', methods=['GET', 'POST'])
# @login_required
def edit_profile():
    user = models.User.get(current_user.id)
    form = forms.EditUserForm()
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.location = form.location.data
        user.save()
        flash('Success! Changes saved.')

        return redirect(url_for('profile', username=user.username))
    return render_template('edit-profile.html', form=form, user=user)
#==============
# Create Resource route
# =============
# @app.route('/create-resource', methods=['GET', 'POST'])
# @login_required
# def add_resource():
#     form = forms.ResourceForm()
#     user = g.user._get_current_object()

#     models.Resource.create(
#         category = form.category.data,
#         title = form.title.data,
#         content = form.content.data
#         # user = g.user._get_current_object()
#         resource = models.Resource.get(models.Resource.title == form.title.data) 
#     flash('Success!' 'Resource created!')
#     return redirect(url_for ('resource', resource_id=resource.id))   
# else:
#     retuen render_template('create-resource.html', form=form, user=user) 

 









# @app.route('/resources', methods=['GET','PUT'])
# # @app.route('/resources/,resource_id>', methods=['GET', 'PUT'])
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
    return redirect(url_for('index'))


if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)   