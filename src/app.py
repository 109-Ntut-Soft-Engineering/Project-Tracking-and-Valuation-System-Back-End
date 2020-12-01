from flask import Flask
from flask_restful import Api
from flask_cors import CORS
import config
from resources.user_resource import UserResource
from resources.project_resource import ProjectResource
from resources.git_repository_resource import GitRepositoryResource
app = Flask("soft engineering")
app.config.from_object(config)
api = Api(app)
CORS(app, origin='*')

api.add_resource(UserResource, '/user', endpoint='users')
api.add_resource(UserResource, '/user/<string:uid>', endpoint='user')
api.add_resource(ProjectResource, '/project', endpoint='projects')
api.add_resource(ProjectResource, '/project/<string:name>', endpoint='project')
api.add_resource(GitRepositoryResource, '/repository', endpoint='repositories')
api.add_resource(GitRepositoryResource, '/repository/<string:pid>/<string:name>', endpoint='repository')

if __name__ == "__main__":
    app.run()