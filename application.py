from flask import Flask, request, render_template
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv; load_dotenv()
import gunicorn
import os

import bot

application = app = Flask(__name__, static_url_path='', static_folder='static')
app.url_map.strict_slashes = False
app.config['SECRET_KEY'] = os.urandom(24)
app.config['TEMPLATES_AUTO_RELOAD'] = True

#==============================

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class LinkModel(db.Model):
    __tablename__ = 'links'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), unique=True, nullable=False)
    link = db.Column(db.String(), unique=True, nullable=False)
    tweeted = db.Column(db.Boolean())

    def __repr__(self):
        return f'<Title: {self.title.strip()}>'
    
    def serialize(self):
        return {
            'id': self.id, 
            'title': self.title,
            'link': self.link
        }

#==============================

PASSWORD = os.getenv('PASSWORD')

#==============================

def requirePW(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.form.get('password') != PASSWORD:
            return app.send_static_file('invalid.html')
        return f(*args, **kwargs)
    return decorated_function

@app.errorhandler(404)
def page_not_found(e):
    return app.send_static_file('index.html'), 200

@app.route('/home', methods=['GET'])
def home():

    return app.send_static_file('index.html'), 200

@app.route('/search', methods=['POST'])
@requirePW
def search():

    results = bot.executeBlock(db, LinkModel)

    if not isinstance(results, list):
        return app.send_static_file('failed.html')
    else:
        return render_template('choose.html', data=results, length=len(results))

@app.route('/tweet', methods=['POST'])
@requirePW
def tweet():

    idList = [int(i) for i in request.form.getlist('urlchoices')]
    status = bot.tweetFunc(idList, db, LinkModel)

    if status == 200:
        return app.send_static_file('passed.html')
    else:
        return app.send_static_file('failed.html')
    

#==============================
if __name__ == "__main__":
    app.run(debug=False)
