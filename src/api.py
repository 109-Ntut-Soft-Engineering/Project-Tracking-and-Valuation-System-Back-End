from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from routes.example_controller import ExampleController


class DevConfig(object):
    DEBUG = True


app = Flask("soft engineering")
app.config_class(DevConfig)
api = Api(app)
CORS(app, origin='*')

api.add_resource(ExampleController, '/example/')


if __name__ == "__main__":
    app.run()