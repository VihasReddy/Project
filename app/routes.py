from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, EmpDetails
from werkzeug.urls import url_parse

from app import app, db
from app.forms import LoginForm, Details


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/index')
@login_required
def index():
    return render_template('index.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/update_skill', methods=['GET', 'POST'])
def update_skill():
    form = Details()
    if form.validate_on_submit():
        row = EmpDetails(emp_id=form.emp_id.data, skill=form.skills.data, experience=form.experience.data,
                         emp_rating=int(form.emp_rating.data))
        db.session.add(row)
        db.session.commit()
        print(int(form.emp_rating.data))
        return redirect(url_for('login'))
    return render_template('update_skill.html', title='Register', form=form)
