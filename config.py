import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    #crypto key used to generate tokens and signatures
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'once-in-a-blue-moon'

    #for the location of the database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #Mail config in the case of sending realtime logs from the production server
    # MAIL_SERVER = os.environ.get('MAIL_SERVER')
    # MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    # MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    # ADMINS = ['barmuriat@gmail.com']

    #Pagination settings
    POSTS_PER_PAGE = 5  