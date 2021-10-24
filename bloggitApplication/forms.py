from flask_wtf import FlaskForm 
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, Email, EqualTo, email_validator  
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextField 
from bloggitApplication.models import User
from werkzeug.routing import ValidationError
from flask_login import current_user

class RegisterForm(FlaskForm):
    username = StringField('User Name', validators = [DataRequired(), Length(min =2, max = 40)]) 
    email = StringField('Email ID', validators = [DataRequired(), Email()])  
    password = PasswordField('Password', validators = [DataRequired()]) 
    confirm_password = PasswordField('Confirm Password', validators = [DataRequired(), EqualTo('password')]) 
    submit = SubmitField('Sign Up') 

    def validate_username(self, username): 
        user_flag = User.query.filter_by(username=username.data).first() 
        if user_flag:
            raise ValidationError('Username exists!') 

    def validate_email(self, email):
        user_email = User.query.filter_by(email=email.data).first()
        if user_email:
            raise ValidationError('Email exists!') 

class LoginForm(FlaskForm):
    email = StringField('Email ID', validators = [DataRequired(), Email()])     
    password = PasswordField('Password', validators = [DataRequired()]) 
    remember = BooleanField('Remember Me') 
    submit = SubmitField('Log In') 


class profileUpdateForm(FlaskForm):
    username = StringField('User Name', validators = [DataRequired(), Length(min =2, max = 40)]) 
    email = StringField('Email ID', validators = [DataRequired(), Email()]) 
    display_pic = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])  
    submit = SubmitField('Save Changes') 

    def validate_username(self, username): 
        user_flag = User.query.filter_by(username=username.data).first() 
        print(f'Username = {username.data} and current_user.username = {current_user.username}')
        if user_flag and username.data != current_user.username:
            raise ValidationError('Username exists!') 

    def validate_email(self, email):
        user_email = User.query.filter_by(email=email.data).first()
        print(f'Username = {email.data} and current_user.username = {current_user.email}')
        if user_email and email.data != current_user.email:
            raise ValidationError('Email exists!')


class PostContentForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextField('Content', validators=[DataRequired()])
    submit = SubmitField('Save Changes')

class RequestResetForm(FlaskForm):
    email = StringField('Email ID', validators = [DataRequired(), Email()])
    submit = SubmitField('Make Reset Request')

    def validate_email(self, email):
        user_person = User.query.filter_by(email=email.data).first()
        if user_person is None:
            raise ValidationError('Email ID does not exist!')

class ResetPasswordForm(FlaskForm):
    new_password = PasswordField('New Password', validators= [DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(),EqualTo('new_password')])
    submit = SubmitField('Reset Password Now')
