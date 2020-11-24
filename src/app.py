from flask import Flask
from flask_restful import Api
from flask_cors import CORS
import config
from resources.example_controller import ExampleController
from resources.user_resource import UserResource
from resources.project_resource import ProjectResource

app = Flask("soft engineering")
app.config.from_object(config)
api = Api(app)
CORS(app, origin='*')

api.add_resource(ExampleController, '/example/')
api.add_resource(UserResource, '/user', endpoint='users')
api.add_resource(UserResource, '/user/<string:uid>', endpoint='user')
api.add_resource(ProjectResource, '/project/', endpoint='projects')
api.add_resource(ProjectResource, '/project/<string:pid>', endpoint='project')

if __name__ == "__main__":
    app.run()