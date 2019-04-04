import datetime
from peewee import *
# import os 
# from flask import jsonify 
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash

DATABASE = SqliteDatabase('mom.db') #sets db variable for development

class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=100)
    location = TextField()
    image_filename = CharField() 
    image_url = CharField() 
    
    class Meta:
        database = DATABASE
        db_table = 'user' 

     #signup (POST)   
    @classmethod
    def create_user(cls, username, email, password, location, image_filename, image_url):
        try:
            cls.create(
                username = username,
                email = email,
                password = generate_password_hash(password),
                location = location,
                image_filename = image_filename,
                image_url = image_url
            ) 
                
        except IntegrityError:
            raise ValueError("User already exists")

    @classmethod
    def edit_user(cls, username, email, password, location):
        try:
            cls.create(
                username = username,
                email = email,
                password = generate_password_hash(password),
                location = location 
            )
        except IntegrityError:
            raise ValueError("edit error")
            
class Resources(Model):
    category = CharField()
    title = CharField()
    content = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now())
    user = ForeignKeyField(User, backref="resources")
    
    class Meta:
        database = DATABASE
        db_table = 'resources'
        order_by = ['-timestamp']

@classmethod
def create_resource(cls, category, title, content, timestamp, userId): #??Add ID???
    try:
        cls.create(
            category = category,
            title = title,
            content = content,
            timestamp = timestamp,
            user = user
        )
    
    except IntegrityError:
        raise ValueError("create resource error")   

class SavedResources(Model):
    user = ForeignKeyField(User)
    resource = ForeignKeyField(Resources) 
    timestamp = DateTimeField(default=datetime.datetime.now())

    class Meta:
        database = DATABASE
        db_table =  'savedResources'
        order_by = ['-timestamp']



def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Resources, SavedResources], safe=True)
    DATABASE.close()