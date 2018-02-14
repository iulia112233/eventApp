import os

SECRET_KEY = 'secret'
#os.urandom(32)
basedir = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = './static/img/'
GALLERY_FOLDER = './static/gallery/'
DEFAULT_EVENT_IMAGE = 'events-default.jpg'
MAIL_SERVER = ''
MAIL_PORT = ''
MAIL_USERNAME = ''
MAIL_PASSWORD = ''
MAIL_USE_TLS = False
MAIL_USE_SSL = False
ADMINS = []
STRIPE_PK = ''
STRIPE_SK = ''

 
SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root:root@localhost:3306/bd'

