import datetime
from peewee import *

from flask_login import UserMixin
from flask_bcrypt import generate_password_hash 
# import os 
# from wtforms import SelectField

DATABASE = SqliteDatabase('mom.db') #sets db variable for development

class User(UserMixin, Model):
    
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=50)
    location = CharField()
    
    
    class Meta:
        database = DATABASE
        order_by = ('-username',)
         

     #signup (POST)   
    @classmethod
    def create_user(cls, username, email, password, location):
        try:
            cls.create(
                username = username,
                email = email,
                password = generate_password_hash(password),
                location = location)
                
        except IntegrityError:
            raise ValueError("User already exists")

    @classmethod
    def edit_user(cls, username, email, password, location):
        try:
            cls.create(
                username = username,
                email = email,
                password = generate_password_hash(password),
                location = location) 
           
        except IntegrityError:
            raise ValueError("edit error")
            
class Resources(Model):
    user = ForeignKeyField(
        model = User,
        backref='resources'        
    )
    category = CharField()
    title = CharField()
    content = CharField()
    timestamp = DateTimeField(default=datetime.datetime.now())
    
    class Meta:
        database = DATABASE
        order_by = ('-timestamp')

    @classmethod
    def create_resource(cls,user, category, title, content):  
        try:
            cls.create(
                user = user,
                category = category,
                title = title,
                content = content
            )
    
        except IntegrityError:
            raise ValueError("create resource error")   

class SavedResources(Model):
    user = ForeignKeyField(User) 
    resource = ForeignKeyField(Resources)
    timestamp = DateTimeField(default=datetime.datetime.now())

    class Meta:
        database = DATABASE
        order_by = ('-timestamp')
        # indexes = ((("user", "resource"), True),)

    @classmethod
    def save_resource(cls, user, resource):  
        try:
            cls.create(
                user = user,
                resource = resource
            )
        except IntegrityError:
            raise



def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Resources, SavedResources], safe=True)
    DATABASE.close()