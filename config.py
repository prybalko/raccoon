from os.path import abspath, dirname, join


PROJECT_DIR = abspath(dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + join(PROJECT_DIR, 'raccoon.db')

SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = 'hwalMbsbxIT9CscaVNO9a9l4XYLnaTOx'

MAIL_SERVER = 'smtp.yandex.ru:465'
MAIL_USERNAME = 'raccoon.info@yandex.ru'
MAIL_PASSWORD = 'BGvv!jg60e0O'
