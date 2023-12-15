from flask import Flask
from .extensions import mongo
from .routes.main import main
from .routes.users import user
from .routes.custumers import custumer
from .routes.categories import category

def create_app(config_object='api.settings'):
    app = Flask(__name__)
    app.config.from_object(config_object)
    app.register_blueprint(user)
    app.register_blueprint(custumer)
    app.register_blueprint(main)
    app.register_blueprint(category)
      
    mongo.init_app(app)
    return app