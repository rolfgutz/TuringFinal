import os.path
basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
<<<<<<< HEAD
=======

SECRET_KEY = "secret"
>>>>>>> 8a8b6761542d3ee2cf0ddf5b8f2785f06e1c3cab
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'banco.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = 'secret'

