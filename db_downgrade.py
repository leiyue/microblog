#!env/Scripts/python
# -*- coding: utf-8 -*-
# @Date    : 2016-01-21 14:59
# @Author  : leiyue (mr.leiyue@gmail.com)
# @Link    : https://leiyue.wordpress.com/

from migrate.versioning import api
from config.default import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO


version = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
api.downgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, version - 1)
version = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
print('Current database version: %03d' % str(version))
