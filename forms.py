from flask_wtf import FlaskForm as Form 
from models import User, Resources
from wtforms import StringField, PasswordField, TextAreaField, SelectField
from wtforms.validators import (DataRequired, Regexp, ValidationError, Email, Length, EqualTo)
from flask_wtf.file import FileField, FileRequired, FileAllowed

class UploadForm(Form):
    file = FileField(FileRequired()) 

def name_exists(form, field):
    if User.select().where(User.username == field.data).exists():
        raise ValidationError('Try Again! Username already exists.')

def email_exists(form,field):
    if User.select().where(User.email == field.data).exits():
        raise ValidationError('Try Again! Email already exists.')

class SignUpForm(Form):
    username = StringField(
       'Username',
       validators=[
           DataRequired(),
           Regexp(
               r'^[a-zA-Z0-9_]+$',
                message=("Username invalid. Use letters, "
                         "numbers 0-9, and underscores only.")
           ),
           name_exists
        ])
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(),
            email_exists
        ]) 
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=5),
            EqualTo('password2', message='Password must match!')
        ])
    password2 = PasswordField(
        'Confirm Password',
        validators=[DataRequired()]
    )

    location = StringField(
        'Location'
        validators=[
            DataRequired()
        ])
    profile_image = FileField('Profile Image') 


class SignInForm(Form): 
    email = StringField('Email', Validators=[DataRequired(), Email()])    
    password = PasswordField('Password', validators=[DataRequired()]) 

class EditUserForm(Form):
    username = StringField('Username')
    email = StringField('Email')
    location = StringField('Location')

class ResourceForm(Form):
    category = SelectField(
        'Category',
        choices=[('technical','Technical'), ('non-technical', 'Non-Technical')]
        validators=[DataRequired()]
        )
    title = StringField(
        'Title',
        validators=[DataRequired()]
        )
    content = TextAreaField(
        'Resources and Events',
        validators=[DataRequired()]
        )

class EditResourcesForm(Form):
    category = SelectField('Category', choices=[('technical', 'Technical'), ('non-technical', 'Non-Technical')])
    title = SelectField('Title')
    content = TextAreaField('Content')