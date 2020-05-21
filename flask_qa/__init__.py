from flask import Flask, redirect, url_for
from .extensions import db, login_manager
from .commands import create_tables
from .routes.main import main
from .routes.auth import auth
from .models import User

@login_manager.user_loader
def create_app(config_file = 'settings.py'):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = ''
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.cli.add_command(create_tables)
    return app
@auth.route('/logout')
def logout():
    # logout_user()
    return redirect(url_for('auth.login'))