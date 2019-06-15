import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'not_for_deployment'
    UPLOAD_FOLDER = 'uploads'
    IMAGE_FOLDER = '../images'
