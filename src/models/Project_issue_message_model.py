from utilities.github_api_requester import GithubApiRequester
from conn_tool import ConnTool


class ProjectIssueMessageModel():
    def __init__(self, id_token):
        _conn_tool = ConnTool(id_token)
        self._db = _conn_tool.db
        self._uid = _conn_tool.uid

    def get_issues(self, name, token):
        project = self.__get_project(name)
        urls = self.__get_repositories_urls(project)

        requester = GithubApiRequester('ef4164107b7e4e2505abd8fced70951f44e51964')
        issues = []
        for url in urls:
            # 用url拿到rp
            repo = {}
            print('url', url)
            rp = requester.get_rp_by_rul(url)
            repo['name'] = rp.name
            if rp is None:
                pass
            else:
                # get_stats_code_frequency 可以換成你要的
                # 先不要用get_rp_info 他會撈code_freq, issues, commits會有點久
                issue = requester.get_issues(rp)
                repo['issue'] = issue
            issues.append(repo)
        return issues

    def __get_project(self, name):
        project = self.__get_unique(self._db.collection(u'projects').where(u'name', u'==', name)).to_dict()
        return project

    def __get_repositories_urls(self, project):
        urls = []
        sources = project[u'repositories']
        try:
            for source_key in sources.keys():
                for url in sources[source_key]:
                    urls.append(url)
        except :
                print("get repository occur error.")
        return urls

    def __get_unique(self, collection):
        return next(collection.stream())

