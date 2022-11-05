import os
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SESSION TYPE'] = 'filesystem'

    app.config.from_mapping(
            SECRET_KEY = 'Mykey',
            DATABASE_HOST = os.environ.get('FLASK_DATABASE_HOST'),
            DATABASE_PASSWORD = os.environ.get('FLASK_DATABASE_PASSWORD'),
            DATABASE_USER = os.environ.get('FLASK_DATABASE_USER'),
            DATABASE = os.environ.get('FLASK_DATABASE')
        )

    from . import db

    db.init_app(app)

    from . import auth
    from . import main 

    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)
    
    return app

app = create_app()

