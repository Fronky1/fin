import os

from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate

from config import Config
from models import db

app = Flask(__name__)
app.config.from_object(Config)

# создаём папку для фото
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Войдите, чтобы добавить рецепт или оставить комментарий'
login_manager.login_message_category = "info"

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))  # User не импортирован



from routes import *

if __name__ == '__main__':
    app.run()