from utilities.github_api_requester import GithubApiRequester
from conn_tool import ConnTool
import datetime
from models.user_model import UserModel


class ProjectWeekCommitModel():
    def __init__(self):
        _conn_tool = ConnTool()
        self._db = _conn_tool.db
        self._uid = _conn_tool.uid
        self._userModel = UserModel(_conn_tool)

    def get_weekcommit(self, pid):
        project = self.__get_project(pid)
        repositories_id = project['repositories']['Github']

        token = self._userModel.get_user_githubToken()
        requester = GithubApiRequester(token)

        repos_commits = []
        for id in repositories_id:
            rp = requester.get_rp_by_id(id)
            if rp is None:
                pass
            else:
                repos_commits.append(requester.get_weekcommit(rp))

        all_repo_week_commit = self.__create_repo_week_dict()

        for repo_commits in repos_commits:
            if repo_commits['start_time'] < all_repo_week_commit['start_time']:
                all_repo_week_commit['start_time'] = repo_commits['start_time']
            if repo_commits['end_time'] > all_repo_week_commit['end_time']:
                all_repo_week_commit['end_time'] = repo_commits['end_time']
            for commit_info in repo_commits['commit_info']:
                self.__calculate_commit_times(
                    all_repo_week_commit['commit_info'], commit_info)
        print(all_repo_week_commit)
        return all_repo_week_commit

    def __create_repo_week_dict(self):
        week_dict = {}
        commit_info_list = []
        week_days = ('Monday', 'Tuesday', 'Wednesday',
                     'Thursday', 'Friday', 'Saturday', 'Sunday')
        for week_day in week_days:
            commit_info = {}
            commit_info['week_day'] = week_day
            for hours in range(24):
                commit_info[str(hours).zfill(2)] = 0
            commit_info_list.append(commit_info)

        week_dict['start_time'] = str(datetime.date(2099, 12, 31))
        week_dict['end_time'] = str(datetime.date(1999, 1, 1))
        week_dict['commit_info'] = commit_info_list
        return week_dict

    def __calculate_commit_times(self, week_list: list, commit_info: dict):
        for week_day in week_list:
            if week_day['week_day'] == commit_info['week_day']:
                week_day[commit_info['time']
                         ] = week_day[commit_info['time']] + 1
                break

    def __get_project(self, pid):
        project = self._db.collection(
            u'projects').document(pid).get().to_dict()

        return project
