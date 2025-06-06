from flask import Blueprint, render_template
from auth import role_required
from flask import Flask, render_template, request,  jsonify, send_file
from models import author_submission, db
from datetime import date
import time
from io import BytesIO

# Get the current system date
current_date = date.today()

print("Current Date:", current_date)
main = Blueprint('main', __name__)

@main.route('/', endpoint='home')
def home():
    return render_template('project1.html')

@main.route('/login')
def login():
    return render_template('login.html')

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/theme')
def theme():
    return render_template('theme.html')

@main.route('/download/<id>')
def download(id):

    paper = db.session.query(author_submission).filter_by(id=id).first()
    if paper:
        return send_file(path_or_file=BytesIO(paper.file_content), mimetype='application/pdf', as_attachment=True, download_name=paper.file_name)
    else:
        return "File not found", 404

@main.route('/delete/<id>')
def delete(id):
    result = db.session.query(author_submission).filter_by(id=id).delete()
    db.session.commit()
    if result:
        return jsonify({"success": True, "message": "Paper deleted successfully"})
    else:
        return jsonify({"success": False, "message": "Paper not found"})
    return render_template('call_for_papers.html')


@main.route('/call_for_papers')
@role_required('admin')
def call_for_papers():
    papers = db.session.query(author_submission).all()
    return render_template('call_for_papers.html', papers=papers, total=len(papers))

@main.route('/paper_submission', methods=['GET', 'POST'])
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

@main.route('/important_dates')
def important_dates():
    return render_template('important_dates.html')

@main.route('/registration')
def registration():
    return render_template('registration.html')

@main.route('/team')
def team():
    return render_template('team.html')

@main.route('/keynote')
def keynote():
    return render_template('keynote.html')

@main.route('/publication')
def publication():
    return render_template('publication.html')

@main.route('/ contact')
def contact():
    return render_template('contact.html')

@main.route('/nearby_locations')
def nearby_locations():
    return render_template('nearby_locations.html')