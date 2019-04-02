from flask_wtf import FlaskForm as Form 
from models import User
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import (DataRequired, Regexp, ValidationError, Email, Length,EqualTo)

def name_exists(form, field):
    if User.select().where(User.username == field.data).exists():
        raise ValidationError('User already exists. Try again!')

class SignUpForm(Form):
    username = StringField(
       'Username',
       validators=[
           DataRequired(),
           Regexp(
               r'^[a-zA-Z0-9_]+$',
                message=("Username invalid. Use letters, "
                         "numbers, and underscores only.")
           ),
           name_exists
        ])
    
   