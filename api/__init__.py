from flask import Flask
from .extensions import mongo
from .routes.user import user

def start_mongo_service():
    import subprocess
    from subprocess import call 
    status = subprocess.check_output("systemctl show -p ActiveState --value mongodb.service",shell=True)
    pwd='er'
    cmd='systemctl start mongodb.service'
    if 'inactive' in str(status):
        call('echo {} | sudo -S {}'.format(pwd, cmd), shell=True)
        print('MONGO STARTED')
    else:
        print('MONGO IS RUNNING')

def create_app(config_object='api.settings'):
    app = Flask(__name__)
    app.config.from_object(config_object)
    app.register_blueprint(user)
    mongo.init_app(app)

    start_mongo_service()
    return app