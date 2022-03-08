from flask import render_template, url_for
from models import db, app, Project


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/project')
def project():
    return render_template('detail.html')


@app.route('/add/project')
def add_project():
    return render_template('projectform.html')


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, port=8000, host='127.0.0.1')


