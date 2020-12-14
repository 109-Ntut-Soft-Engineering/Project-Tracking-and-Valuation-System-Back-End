from utilities.github_api_requester import GithubApiRequester
from conn_tool import ConnTool


class ProjectIssueMessageModel():
    def __init__(self, id_token):
        _conn_tool = ConnTool(id_token)
        self._db = _conn_tool.db
        self._uid = _conn_tool.uid

    def get_issues(self, name, token):
        '''
        project = self.__get_project(name)
        repositories = self.__get_repositories(project)

        requester = GithubApiRequester(token)
        issues = []
        for repository in repositories:
            # 用url拿到rp
            rp = requester.get_rp_by_rul('https://github.com/Gougon-Side-Project/Android-DodoCagePhonograph')
            if rp is None:
                pass
            else:
                # get_stats_code_frequency 可以換成你要的
                # 先不要用get_rp_info 他會撈code_freq, issues, commits會有點久
                issue = requester.get_issues(rp)
                issues.append(issue)
        '''
        requester = GithubApiRequester('ef4164107b7e4e2505abd8fced70951f44e51964')
        rp = requester.get_rp_by_rul('https://github.com/Gougon-Side-Project/Android-DodoCagePhonograph')
        issue = requester.get_issues(rp)
        return issue

    def __get_project(self, name):
        project = self.__get_unique(self._db.collection(u'projects').where(u'name', u'==', name)).to_dict()
        return project

    def __get_repositories(self, project):
        repositories = []
        rids = map(int, project[u'repositories'])
        try:
            for rid in rids:
                repository = self.__get_unique(self._db.collection(u'repositories').where(u'rid', u'==', rid))
                repository = repository.to_dict()
                print('repository:', repository)
                repositories.append(repository)
        except :
                print("get repository occur error.")
        return repositories

    def __get_unique(self, collection):
        return next(collection.stream())

