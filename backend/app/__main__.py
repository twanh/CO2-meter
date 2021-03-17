from flask import Flask, _app_ctx_stack  #type: ignore

from celery import Celery

from sqlalchemy.orm import scoped_session

from . import models
from .database import SessionLocal, engine
# from .tasks import *

models.Base.metadata.create_all(bind=engine) #type: ignore

flask_app = Flask(__name__)

flask_app.session = scoped_session(SessionLocal, scopefunc=_app_ctx_stack.__ident_func__)

# CELERY SETUP

flask_app.config.update(
    CELERY_BROKER_URL='amqp://admin:mypass@localhost:5672',
    CELERY_RESULT_BACKEND='rpc://'
)

celery = Celery(
    flask_app.name,
    backend=flask_app.config["CELERY_RESULT_BACKEND"],
    broker=flask_app.config["CELERY_BROKER_URL"],
)
celery.conf.update(flask_app.config)

from .api import bp as api_bp

flask_app.register_blueprint(api_bp)

@flask_app.teardown_appcontext
def remove_session(*args, **kwags):
    flask_app.session.remove()

if __name__ == '__main__':

    # TODO: Change debug to use env variable
    flask_app.run(debug=True)


