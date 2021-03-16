from flask import Flask, _app_ctx_stack  #type: ignore

from sqlalchemy.orm import scoped_session

from . import models
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine) #type: ignore

app = Flask(__name__)

app.session = scoped_session(SessionLocal, scopefunc=_app_ctx_stack.__ident_func__)

from .api import bp as api_bp

app.register_blueprint(api_bp)

@app.teardown_appcontext
def remove_session(*args, **kwags):
    app.session.remove()

if __name__ == '__main__':

    # TODO: Change debug to use env variable
    app.run(debug=True)


