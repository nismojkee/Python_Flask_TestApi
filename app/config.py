import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    USERNAME = 'tester'
    PASSWORD = 'tester123'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'secret_key'
    UPLOAD_DIR = os.path.join(basedir, '')