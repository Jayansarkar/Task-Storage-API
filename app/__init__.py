import os

from flask_restplus import Api
from flask import Blueprint

from app.main.controller.auth_controller import api as auth_ns
from app.main.controller.task_controller import api as task_ns
from app.main.controller.user_controller import api as user_ns

from app.main import create_app 

blueprint = Blueprint('api', __name__)

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-API-KEY'
    }
}


api = Api(
    blueprint,
    title="Task Storage API",
    version='0.1',
    description="A API for storage of tasks",
    authorizations=authorizations
)

api.add_namespace(auth_ns)
api.add_namespace(task_ns)
api.add_namespace(user_ns)


if __name__ == '__main__':
    app = create_app(os.getenv('RUN_ENV') or 'dev')
    app.register_blueprint(blueprint)
    app.app_context().push()
    app.run()
