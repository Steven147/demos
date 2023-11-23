import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    FLASK_ENV = os.environ.get('FLASK_ENV') or 'development'  # 'development' or 'production'
    FLASK_RUN_PORT = os.environ.get('FLASK_RUN_PORT') or 5000  # the port you want
    # FLASK_RUN_HOST = os.environ.get('FLASK_RUN_HOST') or 'localhost'  # the host ip
    # FLASK_RUN_CERT = os.environ.get('FLASK_RUN_CERT') or None  # the certification file for https
    # FLASK_RUN_KEY = os.environ.get('FLASK_RUN_KEY') or None
    THREADED = os.environ.get('FLASK_RUN_CERT') or True  # enable threading
    SQLALCHEMY_DATABASE_URI = (
            os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'model', 'document.db')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
