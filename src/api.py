from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from src.Routes.example_controller import ExampleController
from src.Routes.git_repository_controller import GitRepositoryController

class DevConfig(object):
    DEBUG = True


app = Flask("soft engineering")
app.config_class(DevConfig)
api = Api(app)
CORS(app, origin='*')

api.add_resource(ExampleController, '/example/')

api.add_resource(GitRepositoryController, '/repository/')


if __name__ == "__main__":
    app.run()