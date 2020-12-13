from resources.project_commit_resource import ProjectCommitResource
from resources.authorization_resource import AuthResource
from resources.repository_resource import RepositoryResource
from resources.project_information_resource import ProjectCodeFrequencyResource
from resources.project_code_frequency_resource import ProjectCodeFrequencyResource
from flask import Flask
from flask_restful import Api
from flask_cors import CORS
import config
from resources.user_resource import UserResource
from resources.projects_resource import ProjectsResource
from resources.project_resource import ProjectResource

app = Flask("soft engineering")
app.config.from_object(config)
api = Api(app)
CORS(app)


api.add_resource(UserResource, '/user')
api.add_resource(ProjectsResource, '/project')
api.add_resource(ProjectResource, '/project/<string:pid>')
api.add_resource(ProjectCommitResource, '/project/<string:name>/commit')
api.add_resource(AuthResource, '/user/auth')

api.add_resource(RepositoryResource, '/repository', endpoint='repositories')


# for code frequency
api.add_resource(ProjectCodeFrequencyResource,
                 '/project/code_freq/<string:name>')
#api.add_resource(GitRepositoryResource, '/repository', endpoint='repositories')
#api.add_resource(GitRepositoryResource, '/repository/<string:pid>/<string:name>', endpoint='repository')
api.add_resource(RepositoryResource, '/user/AvailRepository/<string:pid>')


# for code frequency
# api.add_resource(ProjectCodeFrequencyResource,
#                  '/project/code_freq/<string: project>')

if __name__ == "__main__":
    app.run()
