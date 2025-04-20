from flask import Flask, render_template, request,  jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from io import BytesIO
from sqlalchemy.sql import text
from sqlalchemy.orm import sessionmaker
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
from datetime import date
from author_submission import author_submission, db
import time
from concurrent.futures import ThreadPoolExecutor
from mail_service import mail_service

# Get the current system date
current_date = date.today()

print("Current Date:", current_date)
import os

app = Flask(__name__)

db_name = 'santhiram_clg'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@host.docker.internal:3306/' + db_name
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/' + db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.init_app(app)

mail_service = mail_service(
    smtp_server='smtp.gmail.com',
    smtp_port=587,
    username='emnac2026@gmail.com',
    password='hmzh dtpa raey frzs')

#mail_service.send_email('viswachityala@gmail.com', 'test', 'test')

@app.route('/', endpoint='home')
def home():
    return render_template('project1.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/theme')
def theme():
    return render_template('theme.html')

@app.route('/download/<id>')
def download(id):

    paper = db.session.query(author_submission).filter_by(id=id).first()
    if paper:
        return send_file(path_or_file=BytesIO(paper.file_content), mimetype='application/pdf', as_attachment=True, download_name=paper.file_name)
    else:
        return "File not found", 404
    
@app.route('/delete/<id>')
def delete(id):
    result = db.session.query(author_submission).filter_by(id=id).delete()
    db.session.commit()
    if result:
        return jsonify({"success": True, "message": "Paper deleted successfully"})
    else:
        return jsonify({"success": False, "message": "Paper not found"})
    return render_template('call_for_papers.html')


@app.route('/call_for_papers')
def call_for_papers():
    papers = db.session.query(author_submission).all()
    return render_template('call_for_papers.html', papers=papers, total=len(papers))

@app.route('/paper_submission', methods=['GET', 'POST'])
def paper_submission():
    if request.method == 'GET':
        return render_template('paper_submission.html')
    else:
        title = request.form['title']
        abstract = request.form['abstract']
        keywords = request.form['keywords']
        file = request.files['file']
        data = file.read()
        file_name = file.filename
        print("Title:", title)
        print("Abstract:", abstract)
        print("File name:", file.filename)
        paper_pub = author_submission(title=title, abstract=abstract, keywords=keywords,
                                      file_content=data, file_name=file_name, submission_date=current_date, 
                                      author_name="Author Name", 
                                      user_name="User Name")
        
        print(f"started at: {time.strftime('%X')}")
        db.session.add(paper_pub)
        db.session.commit()
        print(f"ended at: {time.strftime('%X')}")
        return render_template('paper_submission.html')
    
@app.route('/important_dates')
def important_dates():
    return render_template('important_dates.html')

@app.route('/registration')
def registration():
    return render_template('registration.html')

@app.route('/team')
def team():
    return render_template('team.html')

@app.route('/keynote')
def keynote():
    return render_template('keynote.html')

@app.route('/publication')
def publication():
    return render_template('publication.html')

@app.route('/ contact')
def contact():
    return render_template('contact.html')

@app.route('/nearby_locations')
def nearby_locations():
    return render_template('nearby_locations.html')

app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/files'

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)