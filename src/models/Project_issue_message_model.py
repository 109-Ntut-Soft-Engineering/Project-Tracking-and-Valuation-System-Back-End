from utilities.github_api_requester import GithubApiRequester
from models.user_model import UserModel


class ProjectIssueMessageModel():
    def __init__(self, conn_tool):
        self._db = conn_tool.db
        self._uid = conn_tool.uid
        self._userModel = UserModel(conn_tool)

    def get_issues(self, pid):
        project = self.__get_project(pid)
        if project == None:
            return {}
        repositories_id = project['repositories']['Github']

        token = self._userModel.get_user_githubToken()
        requester = GithubApiRequester(token)
        issues = []
        for id in repositories_id:
            repo = {}
            rp = requester.get_rp_by_id(id)
            repo['name'] = rp.name
            if rp is not None:
                issue = requester.get_issues(rp)
                repo['issue'] = issue

            issues.append(repo)
        return issues

    def __get_project(self, pid):
        project = self._db.collection(
            u'projects').document(pid).get().to_dict()
        return project
