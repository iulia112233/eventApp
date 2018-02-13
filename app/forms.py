from flask_wtf import Form
from wtforms import StringField, BooleanField, PasswordField, FileField, TextAreaField
from wtforms.validators import DataRequired, EqualTo 

class LoginForm(Form):
    username = StringField('username')
    password = PasswordField('password')
    remember_me = BooleanField('remember_me')

class RegistrationForm(Form):
    username = StringField('username')
    password = PasswordField('New Password')
    confirm_password = PasswordField('Repeat Password')

class EditForm(Form):
    name = StringField('name')
    surname = StringField('surname')
    image = FileField('image')
    aboutme = TextAreaField('About Me')

    def __init__(self, data, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        if 'name' in data:
            self.name.data = data['name']
        if 'surname' in data:
            self.surname.data = data['surname']

class ResetForm(Form):        
    oldpassword = PasswordField('Old Password', validators=[DataRequired()])
    password = PasswordField('New Password', validators = [
         EqualTo('confirm', message = 'Passwords must match'),
         DataRequired()
        ])
    confirm = PasswordField('Repeat Password')


