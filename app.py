from flask import Flask, g 
from flask import render_template, flash, redirect, url_for
import json 

DEBUG = True
PORT = 8000

app = Flask(__name__) 
app.secret_key = 'molokai'


@app.route('/')
def index():
    return render_template('landing.html')  

@app.route('/about')
def about():
    return render_template('about.html')







if __name__ == '__main__':
    app.run(debug=DEBUG, port=PORT)  