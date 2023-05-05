import logging
logger = logging.getLogger(__name__)

# General packages
import os
import datetime
from flask import Flask
from flask_migrate import Migrate
# SQL-Alchemy model variables
from flask_sqlalchemy import SQLAlchemy
SQLDB = SQLAlchemy()

# -------------------------------------------------------
# App configuration
# -------------------------------------------------------
class CommonConfig(object):

    # Authentication and session
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = True
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(hours=5)
    SESSION_FILE_THRESHOLD = 500

    # SQL-Alchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_DATABASE_URI = 'sqlite:///employees.db'
    SQLALCHEMY_BINDS = {
        'backend': SQLALCHEMY_DATABASE_URI,
    }

class DevelopmentConfig(CommonConfig):
    """
    Development environment configuration
    """
    ENV = 'development'
    DEBUG = True
    TESTING = False

APP_CONFIG = {
    'development': DevelopmentConfig,
}

# -------------------------------------------------------
# Create the App
# -------------------------------------------------------
def create_app():
    # Create Flask application
    app = Flask(__name__)
    # Configure the Flask application
    flask_env = os.getenv('FLASK_ENV')
    if flask_env is None:
        flask_env = 'development'
        logger.warning("FLASK_ENV was not specified, setting to 'development' now:")
        logger.warning("FLASK_ENV: {:}".format(flask_env))
    else:
        logger.info("FLASK_ENV: {:}".format(flask_env))
    app.config.from_object(APP_CONFIG[flask_env])

    ## Initialize SQL-Alchemy support
    SQLDB.init_app(app)
    logger.info("<<<<<<<<< Creating application: Finished <<<<<<<<<")
    return app

# Create the app
APP = create_app()

# -------------------------------------------------------
# API-routes
# -------------------------------------------------------
from employee_view import muvid_api
APP.register_blueprint(muvid_api, url_prefix='/api/v1', name='api')

from prediction_model import muvid_api_prediction
APP.register_blueprint(muvid_api_prediction, url_prefix='/api/v1', name='api_prediction')

migrate = Migrate()
migrate.init_app(APP, SQLDB)
# -------------------------------------------------------
# Run as script
# -------------------------------------------------------
if __name__ == '__main__':
    if APP.config.get('ENV') == 'development':
        APP.run(threaded=True)