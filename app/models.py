from app import db
from app import login
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin


@login.user_loader
def load_user(id):
    return User.query.get(id)


class User(UserMixin, db.Model):
    id = db.Column(db.String(24), primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    overall_exp = db.Column(db.Integer, index=True, nullable=True)
    manager_id = db.Column(db.String(24))
    employees = db.relationship('EmpDetails', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User : {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class EmpDetails(db.Model):
    id1 = db.Column(db.Integer, primary_key=True, autoincrement=True)
    emp_id = db.Column(db.String(24), db.ForeignKey('user.id'))
    skill = db.Column(db.String(24), index=True)
    experience = db.Column(db.Integer, index=True)
    emp_rating = db.Column(db.Integer, index=True)
    manager_rating = db.Column(db.Integer, index=True)

    def __repr__(self):
        return '<Employee ID : {}>'.format(self.emp_id)

