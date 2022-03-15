from flask import (render_template, url_for, request, redirect, flash, jsonify)
from flask_login import login_user, logout_user, current_user, login_required 
from models import db, app, Project, User
from werkzeug.urls import url_parse
from forms import LoginForm
import requests
import datetime



@app.route('/')
def index():
    projects = Project.query.all()
    return render_template('index.html', projects=projects, isIndex=True)


@app.route('/about')
def about():
    projects = Project.query.all()
    return render_template('about.html', projects=projects)


@app.route('/project/<id>')
def project(id):
    projects = Project.query.all()
    single_project = Project.query.get_or_404(id)
    return render_template('detail.html', project=single_project, projects=projects)


@app.route('/project/add', methods=['GET', 'POST'])
def add_project():
    if request.form:
        new_project = Project(
            title=request.form['title'],
            description=request.form['desc'],
            link=request.form['github'],
            skills=request.form['skills'],
            completed=datetime.datetime.strptime(request.form['date'], '%Y-%m')
        )
        db.session.add(new_project)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('projectform.html')


@app.route('/project/<id>/edit', methods=['GET', 'POST'])
def edit_project(id):
    projects = Project.query.all()
    project = Project.query.get_or_404(id)
    if request.form:
        project.title = request.form['title']
        project.description = request.form['desc']
        project.link = request.form['github']
        project.skills = request.form['skills']
        project.completed = datetime.datetime.strptime(request.form['date'], '%Y-%m')
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('editproject.html', project=project, projects=projects)


@app.route('/project/<id>/delete')
def delete_project(id):
    single_project = Project.query.get_or_404(id)
    db.session.delete(single_project)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/articles')
def articles():
    articles = requests.get('https://dev.to/api/articles?username=grahammorby')
    articles = articles.json()
    return render_template('articles.html', articles=articles)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'alert-danger')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)
        

@app.route('/register', methods=['POST'])
def register():
    user = User(username=request.form['username'], email=request.form['email'])
    user.set_password(request.form['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify(message='User successfully added'), 200


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', msg=error), 404


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, port=8000, host='127.0.0.1')
