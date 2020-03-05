from app import db, app, login
from time import time
import jwt
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

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode({'reset_password': self.id, 'exp': time() + expires_in},
                          app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


class EmpDetails(db.Model):
    id1 = db.Column(db.Integer, primary_key=True, autoincrement=True)
    emp_id = db.Column(db.String(24), db.ForeignKey('user.id'))
    skill = db.Column(db.String(24), index=True)
    experience = db.Column(db.Integer, index=True)
    emp_rating = db.Column(db.Integer, index=True)
    manager_rating = db.Column(db.Integer, index=True)

    def __repr__(self):
        return '<Employee ID : {}>'.format(self.emp_id)
