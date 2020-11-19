from flask import Flask
from flask_restful import Api
from flask_cors import CORS
import common.config as config
from resources.example_controller import ExampleController

app = Flask("soft engineering")
app.config.from_object(config)
api = Api(app)
CORS(app, origin='*')

api.add_resource(ExampleController, '/example/')


if __name__ == "__main__":
    app.run()