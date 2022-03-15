from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
db = SQLAlchemy(app)
login = LoginManager(app)


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


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))