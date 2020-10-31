#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class BaseConfig(object):
    SERVER_NAME = 'micro-proctoring.ru'
    APPLICATION_ROOT = ''

    SECRET_KEY = 'secret_key'
    DEBUG = False
    SECURITY_PASSWORD_SALT = 'secret_key2'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'
    STORAGE_PATH = './storage'
    MAX_RECORD_LENGTH = 3*60*60 #3h in seconds
    PHOTO_MAX_GAP = 30 # 20seconds -- not more than 3 photo a minute
    PHOTO_MIN_GAP = 20
    GAP_FACTOR = 1.5 # acceptable timedelta deviation

class DevelopConfig(BaseConfig):
    SERVER_NAME = 'localhost:5000'
    APPLICATION_ROOT = ''
    DEBUG = True
    STORAGE_PATH = './storage'

