from app import app, db
from app.forms import LoginForm, RegistrationForm, MessageForm
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user
from app.models import User
from werkzeug.urls import url_parse
from flask_mail import Mail, Message
import os


app.config['MAIL_PASSWORD']= os.environ.get('MOT_DE_PASSE')
app.config['MAIL_SERVER']='smtp.office365.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'theotim@outlook.fr'
app.config['MAIL_PASSWORD'] = 'Intelligence97'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index.html'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index.html')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/menu')
def carte():
    return render_template('carte.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = MessageForm()
    if request.method == 'POST':
        if form.validate() == False:
            flash('Remplir tous les champs')
            return render_template('contact.html', form=form)
        else:
            msg = Message(form.sujet.data, sender='theotim@outlook.fr', recipients=['theotim@outlook.fr'])
            msg.body = "Nom = {}, mail = {}, msg = {}".format(form.nom.data, form.email.data, form.message.data)
            mail.send(msg)
            return render_template('index.html')

    elif request.method == 'GET':
        return render_template('contact.html', form=form)
