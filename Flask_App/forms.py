from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from Flask_App.models import User

class RegistrationForm(FlaskForm):
    
    username = StringField('Username',
                            validators = [DataRequired(), Length(min=2, max=32)])
    email = StringField('Email',
                            validators = [DataRequired(), Email()])
    password = PasswordField('Password',
                            validators = [DataRequired()] )
    confirmPassword = PasswordField('ComfirmPasswod',
                            validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField('SignUp')

    def validate_username(self,username):

        user = User.query.filter_by(username=username.data).first()

        if user:
            raise ValidationError('This username has already taken. PLease choose username!')

    def validate_email(self,email):

        email = User.query.filter_by(email=email.data).first()

        if email:
            raise ValidationError('This email has already taken. Try different email!')


class LoginForm(FlaskForm):
   
    email = StringField('Email',
                            validators = [DataRequired(), Email()])
    password = PasswordField('Password',
                            validators = [DataRequired()] )
    remember = BooleanField('Remember Me')

    submit = SubmitField('Login')