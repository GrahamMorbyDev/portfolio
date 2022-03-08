from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
db = SQLAlchemy(app)


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column('Created', db.DATETIME, default=datetime.datetime.now)
    title = db.Column('Title', db.String)
    description = db.Column('Description', db.TEXT)
    link = db.Column('Link', db.String)
    completed = db.Column('Completed', db.DATETIME)
    skills = db.Column('Skills', db.String)

    def __repr__(self):
        print(f'''
            Project<(Title: {self.title}
            Description: {self.description}
            Link: {self.link}
            Skills: {self.skills}
            Completed: {self.completed}
            Created: {self.created})>
        ''')
