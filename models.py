import datetime
from peewee import *

from flask_login import UserMixin
from flask_bcrypt import generate_password_hash

DATABASE = SqliteDatabase('mom.db')

class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=100)
    location = TextField()
    image_filename = Charfield()
    image_url = CharField 
    
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
                
        except IntegrityError:
            raise ValueError("User already exists")
            
class Resources(Model):
    #???ID??
    category = CharField()
    title = CharField()
    content = TextField()
    timestamp = DateTimeField(default=datetime.now())
    userId  = ForeignKeyField(User, backref="resources")
    
    class Meta:
        database = DATABASE
        db_table = 'resources'
        order_by = ['-timestamp']

@classmethod
def create_resource(cls, category, title, content, timestamp, userId):



def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Resources, SavedResources], safe=True)
    DATABASE.close()