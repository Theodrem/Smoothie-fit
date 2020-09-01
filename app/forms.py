from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, validators
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Identifiant', validators=[DataRequired()])
    password = PasswordField('Mot de Passe', validators=[DataRequired()])
    remember_me = BooleanField('Se souvenir de moi ')
    submit = SubmitField('Valider')


class RegistrationForm(FlaskForm):
    username = StringField('Identifiant', validators=[DataRequired()])
    email = StringField('Adresse email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de Passe', validators=[DataRequired()])
    password2 = PasswordField(
        'Confirmer mot de passe', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Valider')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Utiliser un autre identifiant.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Adresse email deja utilisé.')

class MessageForm(FlaskForm):
    nom = StringField('Nom', [validators.DataRequired(message='Entrez un nom valide')])
    sujet = StringField('Sujet', [validators.DataRequired(message='Entrez le sujet du mail')])
    email = StringField('Email', [validators.DataRequired(message='Entrez un email'), Email()])
    message = TextAreaField('Message', [validators.DataRequired(message='Entrez un message')])
    envoyer = SubmitField('Envoyer')