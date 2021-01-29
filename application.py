from flask import Flask, request
from dotenv import load_dotenv; load_dotenv()
import gunicorn
import os

import bot

application = app = Flask(__name__, static_url_path='', static_folder='static')
app.url_map.strict_slashes = False
app.config['SECRET_KEY'] = os.urandom(24)

PASSWORD = os.getenv('PASSWORD')

#==============================

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
        status = bot.executeBlock()
    else:
        return app.send_static_file('invalid.html')

    if status == 500:
        return app.send_static_file('failed.html')
    elif status == 200:
        return app.send_static_file('passed.html')

#==============================
if __name__ == "__main__":
    app.run(debug=False)
