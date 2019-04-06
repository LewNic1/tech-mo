from flask_wtf import FlaskForm as Form 
from models import User
from wtforms import StringField, PasswordField, TextAreaField, SelectField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


app = Flask(__name__)

app.config['SECRET_KEY'] = 'molokai'



class SignUpForm(FlaskForm):
    username = StringField('Username', 
                           validators=[DataRequired(), Length(min=5, max=15)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
                                     validators=[DataRequired(), EqualTo('password')]) 
    location = StringField('Location', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

class SignInForm(FlaskForm): 
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])    
    password = PasswordField('Password', validators=[DataRequired()]) 
    remember = BooleanField('Remember Me?')
    submit = SubmitField('Sign In')

class EditUserForm(FlaskForm):
    username = StringField('Username', 
                           validators=[DataRequired(), Length(min=5, max=15)])
    email = StringField('Email'
                        validators=[DataRequired(), Email()])
    location = StringField('Location', 
                           validators=[DataRequired()])
    submit = SubmitField('Done')

class ResourceForm(FlaskForm):
    category = SelectField('Category',
                           choices=[('technical','Technical'), ('non-technical', 'Non-Technical')] 
                           validators=[DataRequired()])
    title = StringField('Title',
                        validators=[DataRequired()])
    content = TextAreaField('Content',
                            validators=[DataRequired()])
    submit = SubmitField('Submit')   

class EditResourcesForm(FlaskForm):
    category = SelectField('Category', 
                           choices=[('technical', 'Technical'), ('non-technical', 'Non-Technical')])
                           validators=[DataRequired()])
    title = StringField('Title'
                        validators=[DataRequired]))
    content = TextAreaField('Content',
                            validators=[DataRequired()])  