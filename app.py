from flask import (render_template, url_for, request, redirect)
from models import db, app, Project


@app.route('/')
def index():
    projects = Project.query.all()
    return render_template('index.html', projects=projects)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/project/<id>')
def project(id):
    single_project = Project.query.get_or_404(id)
    return render_template('detail.html', project=single_project)


@app.route('/add/project', methods=['GET', 'POST'])
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


@app.route('/delete/project/<id>')
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
