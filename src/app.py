from flask import Flask, request
from flask_restful import Api
from flask_cors import CORS
from resources.user_resource import UserResource
from resources.project_repos_resource import ProjectReposResource
from resources.project_setting_resource import ProjectSettingResource
from resources.projects_resource import ProjectsResource
from resources.project_code_frequency_resource import ProjectCodeFrequencyResource
from resources.project_compare_code_frequency_resource import ProjectCompareCodeFrequencyResource
from resources.repository_resource import RepositoryResource
from resources.authorization_resource import AuthResource
from resources.project_commit_resource import ProjectCommitResource
from resources.project_compare_commit_resource import ProjectCompareCommitResource
from resources.project_weekcommit_resource import ProjectWeekCommitResource
from resources.project_Issue_message_resource import ProjectIssueMessageResource
from resources.login_resource import LoginResource
from resources.signup_resource import SignUpResource
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
api.add_resource(LoginResource, '/login')
api.add_resource(SignUpResource, '/signUp')
api.add_resource(ProjectReposResource, '/project/<string:pid>/repos')
api.add_resource(ProjectSettingResource, '/project/<string:pid>/setting')
api.add_resource(RepositoryResource, '/project/AvailRepository/<string:pid>')

# for code frequency
api.add_resource(ProjectCodeFrequencyResource,
                 '/project/<string:pid>/code_freq')

api.add_resource(ProjectCompareCodeFrequencyResource, '/project/compare/<string:pid1>/<string:pid2>/code_freq')

# for total commit
api.add_resource(ProjectCommitResource, '/project/<string:pid>/commit')
api.add_resource(ProjectCompareCommitResource, '/project/compare/<string:pid1>/<string:pid2>/commit')

# for commit contribution
api.add_resource(ProjectWeekCommitResource,
                 '/project/<string:pid>/week_commit')

# for issue message
api.add_resource(ProjectIssueMessageResource, '/project/<string:pid>/issue')


if __name__ == "__main__":
    app.run()
