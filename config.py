import os

SECRET_KEY = 'secret'
#os.urandom(32)
basedir = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = './static/img/'
GALLERY_FOLDER = './static/gallery/'
DEFAULT_EVENT_IMAGE = 'events-default.jpg'
MAIL_SERVER = 'email-smtp.eu-west-1.amazonaws.com'
MAIL_PORT = '587'
MAIL_USERNAME = 'AKIAIF5PHUECDHRYQ4QA'
MAIL_PASSWORD = 'AqCaqA93CQTI2L9kyYKjgTl5xtx9Jd3kfi3tMxQJf0XY'
MAIL_USE_TLS = False
MAIL_USE_SSL = False
ADMINS = ['iulia@phyramid.com']
STRIPE_PK = 'pk_test_c9A05XZrxznbqyFQz3iVSm9R'
STRIPE_SK = 'sk_test_GeyyUpAGfkv3yAGSIR7hQQPQ'

 
SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root:root@localhost:3306/bd'

