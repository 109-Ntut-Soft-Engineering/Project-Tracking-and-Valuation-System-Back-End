from utilities.github_api_requester import GithubApiRequester
from conn_tool import ConnTool


class ProjectIssueMessageModel():
    def __init__(self):
        _conn_tool = ConnTool()
        self._db = _conn_tool.db
        self._uid = _conn_tool.uid

    def get_issues(self, pid):
        project = self.__get_project(pid)
        repositories_id = project['repositories']['Github']
        
        token = ' ef4164107b7e4e2505abd8fced70951f44e51964'
        requester = GithubApiRequester(token)
        issues = []
        for id in repositories_id:
            # 用url拿到rp
            repo = {}
            rp = requester.get_rp_by_id(id)
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
        
    def __get_project(self, pid):
            project = self._db.collection(u'projects').document(pid).get().to_dict()

            return project

