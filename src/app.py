from resources.project_commit_resource import ProjectCommitResource
from resources.authorization_resource import AuthResource
from resources.repository_resource import RepositoryResource
from resources.project_code_frequency_resource import ProjectCodeFrequencyResource
from flask import Flask, request
from flask_restful import Api
from flask_cors import CORS
from resources.user_resource import UserResource
from resources.projects_resource import ProjectsResource
from resources.project_repos_resource import ProjectReposResource
from resources.project_setting_resource import ProjectSettingResource
import config


app = Flask("soft engineering")
app.config.from_object(config)
api = Api(app)
CORS(app)

@app.route('/', methods=['GET'])
def home():
    for i in range(200):
        print('i', i)

    return 'test', 200
api.add_resource(UserResource, '/user')
api.add_resource(ProjectsResource, '/projects')
api.add_resource(AuthResource, '/user/auth')

api.add_resource(ProjectReposResource, '/project/<string:pid>/repos')
api.add_resource(ProjectSettingResource, '/project/<string:pid>/setting')
api.add_resource(RepositoryResource, '/project/AvailRepository/<string:pid>')

# for project information
api.add_resource(ProjectCodeFrequencyResource,
                 '/project/<string:pid>/code_freq')
api.add_resource(ProjectCommitResource, '/project/<string:pid>/commit')


if __name__ == "__main__":
    app.run()
