from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv; load_dotenv()
import gunicorn
import os

import bot

application = app = Flask(__name__, static_url_path='', static_folder='static')
app.url_map.strict_slashes = False
app.config['SECRET_KEY'] = os.urandom(24)

#==============================

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class LinkModel(db.Model):
    __tablename__ = 'links'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    link = db.Column(db.String())

    def __init__(self, title, link):
        self.title = title
        self.link = link

    def __repr__(self):
        return f'<Title: {self.title}>'
    
    def serialize(self):
        return {
            'id': self.id, 
            'title': self.title,
            'link': self.link
        }

#==============================

PASSWORD = os.getenv('PASSWORD')

#==============================

@app.route('/.well-known/acme-challenge/VYS0aL6ksJjVnU8yGnUx74LF66e5PWA6QHWMfMcXunA')
def certificate():
    return app.send_static_file('VYS0aL6ksJjVnU8yGnUx74LF66e5PWA6QHWMfMcXunA')

@app.errorhandler(404)
def page_not_found(e):
    return app.send_static_file('index.html'), 200

@app.route('/home', methods=['GET'])
def home():
    return app.send_static_file('index.html'), 200

@app.route('/tweet', methods=['POST'])
def tweet():

    pwIn = request.form.get('password')

    if pwIn and pwIn == PASSWORD:
        status = bot.executeBlock(databaseInstance = db, tableClass = LinkModel)
    else:
        return app.send_static_file('invalid.html')

    if status == 500:
        return app.send_static_file('failed.html')
    elif status == 200:
        return app.send_static_file('passed.html')

#==============================
if __name__ == "__main__":
    app.run(debug=False)
