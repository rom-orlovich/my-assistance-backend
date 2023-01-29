from flask import Flask
from markupsafe import escape
app=Flask(__name__)

@app.route('/')
def index():
    return 'index'

@app.route('/hey')
def hey():
    return 'hey'







