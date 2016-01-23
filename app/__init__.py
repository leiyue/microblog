# -*- coding: utf-8 -*-
# @Date    : 2016-01-21 12:33
# @Author  : leiyue (mr.leiyue@gmail.com)
# @Link    : https://leiyue.wordpress.com/

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_openid import OpenID
from flask_mail import Mail

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config.default')
app.config.from_pyfile('config.py')
if os.getenv('APP_CONFIG_FILE'):
    app.config.from_envvar('APP_CONFIG_FILE')
db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
oid = OpenID(app, os.path.join(app.config['BASE_DIR'], 'tmp'))
mail = Mail(app)

if not app.debug:
    import logging
    from logging.handlers import SMTPHandler

    credentials = None
    mail_server = app.config['MAIL_SERVER']
    mail_port = app.config['MAIL_PORT']
    admins = app.config['ADMINS']
    mail_username = app.config['MAIL_USERNAME']
    mail_password = app.config['MAIL_PASSWORD']
    if mail_username or mail_password:
        credentials = (mail_username, mail_password)
    mail_handler = SMTPHandler(
            (mail_server, mail_port),
            'd0nny@163.com',
            admins,
            'microblog failure',
            credentials
    )
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler

    file_handler = RotatingFileHandler('tmp/app.log', 'a', 1*1024*1024, 10, 'utf-8')
    file_handler.setFormatter(
            logging.Formatter(
                    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s: %(lineno)d]'
            )
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('microblog startup...')

from app import views, models

