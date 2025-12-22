import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key-2025'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'povaryoshka.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(basedir, 'static', 'uploads')
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB макс. фото
    PERMANENT_SESSION_LIFETIME = timedelta(days=30)