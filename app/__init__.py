from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from config import MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD, ADMINS
import logging
from logging.handlers import SMTPHandler


app = Flask(__name__)
app.jinja_env.add_extension('pypugjs.ext.jinja.PyPugJSExtension')
app.config.from_object('config')
db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
lm.login_message = 'Please log in to access this page. '
mail = Mail(app)
credentials = None

if MAIL_USERNAME and MAIL_PASSWORD:
    credentials = (MAIL_USERNAME, MAIL_PASSWORD)
#mail_handler = SMTPHandler((MAIL_SERVER, MAIL_PORT),
#                            ADMINS[0], ADMINS,
#                            'failure', credentials, ())
#mail_handler.setLevel(logging.ERROR)
#app.logger.addHandler(mail_handler)

print credentials
print app

from app import views
from app import api

