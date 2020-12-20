from utilities.github_api_requester import GithubApiRequester
from conn_tool import ConnTool
import datetime


class ProjectWeekCommitModel():
    def __init__(self, id_token):
        _conn_tool = ConnTool(id_token)
        self._db = _conn_tool.db
        self._uid = _conn_tool.uid

    def get_weekcommit(self, name, token):
        requester = GithubApiRequester(' ef4164107b7e4e2505abd8fced70951f44e51964')
        repos_commits = []
        rp = requester.get_rp_by_rul('https://github.com/Gougon-Side-Project/Android-DodoCagePhonograph')
        if rp is None:
            pass
        else:
            repos_commits.append(requester.get_weekcommit(rp))\
        
        all_repo_week_commit = self.__create_repo_week_dict()

        for repo_commits in repos_commits:
            if repo_commits['start_time'] < all_repo_week_commit['start_time']:
                all_repo_week_commit['start_time'] = repo_commits['start_time']
            if repo_commits['end_time'] > all_repo_week_commit['end_time']:
                all_repo_week_commit['end_time'] = repo_commits['end_time']
            for commit_info in repo_commits['commit_info']:
                self.__calculate_commit_times(all_repo_week_commit['commit_info'], commit_info)

        return all_repo_week_commit

    def __create_repo_week_dict(self):
        week_dict = {}
        commit_info_list = []
        week_days = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')
        for week_day in week_days:
            commit_info = {}
            commit_info['week_day'] = week_day
            commits = []
            for hours in range(24):
                commits_detail = {}
                commits_detail['time'] = str(hours).zfill(2)
                commits_detail['commit'] = 0
                commits.append(commits_detail)
            commit_info['commits'] = commits
            commit_info_list.append(commit_info)

        week_dict['start_time'] = str(datetime.date(2099, 12, 31))
        week_dict['end_time'] = str(datetime.date(1999, 1, 1))
        week_dict['commit_info'] = commit_info_list
        return week_dict

    def __calculate_commit_times(self, week_list: list, commit_info: dict):
        for week_day in week_list:
            if week_day['week_day'] == commit_info['week_day']:
                for commit in week_day['commits']:
                    if commit['time'] == commit_info['time']:
                        commit['commit'] = commit['commit'] + 1
                        break
                break

    def __get_project(self, name):
        project = self.__get_unique(self._db.collection(u'projects').where(u'name', u'==', name)).to_dict()
        return project

    def __get_repositories_url(self, project):
        urls = []
        source = project[u'repositories']
        try:
            for source_key in source:
                for url in source[source_key]:
                    urls.append(url)
        except :
                print("get repository occur error.")
        return urls

    def __get_unique(self, collection):
        return next(collection.stream())

