
import flask
from flask import Flask, render_template, request,  jsonify, send_file
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from io import BytesIO
from sqlalchemy.sql import text
from sqlalchemy.orm import sessionmaker
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
from models import author_submission, user, db
from mail_service import mail_service
import time
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from auth import bcrypt
from event_publisher import socketio

import os

app = Flask(__name__)
#bcrypt = Bcrypt()
login_manager = LoginManager()

db_name = 'santhiram_clg'
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USERNAME = os.getenv('DB_USERNAME', 'krishna')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'Naruto#162')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + DB_USERNAME + ':' + DB_PASSWORD + '@' + DB_HOST + ':3306/' + db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)

from auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

from routes import main as main_blueprint
app.register_blueprint(main_blueprint)

mail_service = mail_service(
    smtp_server='smtp.gmail.com',
    smtp_port=587,
    username='emnac2026@gmail.com',
    password='hmzh dtpa raey frzs')

socketio.init_app(app)

#mail_service.send_email('viswachityala@gmail.com', 'test', 'test')

@app.route('/', endpoint='home')
def home():
    return render_template('project1.html')

app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/files'

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@login_manager.user_loader
def load_user(user_id):
    # Return the user object for the given user_id
    return user.query.get(int(user_id))

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)