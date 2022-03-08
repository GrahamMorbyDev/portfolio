from flask import (render_template, url_for, request, redirect)
from models import db, app, Project


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
            completed=request.form['date']
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
        project.completed = request.form['date']
        db.session.commit()
        return redirect('index')
    return render_template('editproject.html', project=project, projects=projects)


@app.route('/project/<id>/delete')
def delete_project(id):
    single_project = Project.query.get_or_404(id)
    db.session.delete(single_project)
    db.session.commit()
    return redirect(url_for('index'))


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', msg=error), 404


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, port=8000, host='127.0.0.1')
