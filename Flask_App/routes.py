from flask import Flask, render_template, url_for, flash, redirect
from Flask_App import app, db, bcrypt
from Flask_App.forms import RegistrationForm, LoginForm
from Flask_App.models import User, Post
from flask_login import login_user, current_user, logout_user

post = [
    {
        'author':'Ali',
        'title':'Post 1',
        'content':'Creating 1st post',
        'date':'23-10-23'
    },
    {
        'author':'Babar',
        'title':'Post 2',
        'content':'Creating 2nd post',
        'date':'23-10-23'
    }
]

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html',posts= post)

@app.route('/about')
def about():
    return render_template('about.html',title='About')

@app.route('/register', methods = ['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        h_pw = bcrypt.generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=h_pw)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created, Your are now able to login!', 'success')
        
        return redirect(url_for('login'))
    return render_template('register.html',title='Register', form= form)

@app.route('/login', methods = ['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user,remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Login Failed. Please check your email or password!','danger')
    return render_template('login.html',title='Login', form= form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))