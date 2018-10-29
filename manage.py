import os

from app.main import create_app
from app import blueprint

app = create_app(os.getenv('RUN_ENV') or 'dev')

app.register_blueprint(blueprint)
app.app_context().push()


def run():
    app.run()


if __name__ == '__main__':
    run()
