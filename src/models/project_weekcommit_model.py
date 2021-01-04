from utilities.github_api_requester import GithubApiRequester
from conn_tool import ConnTool
import datetime
from models.user_model import UserModel


class ProjectWeekCommitModel():
    def __init__(self, conn_tool):
        self._db = conn_tool.db
        self._uid = conn_tool.uid
        self._userModel = UserModel(conn_tool)

    def get_weekcommit(self, pid):
        project = self.__get_project(pid)
        if project == None :
            return {}

        repositories_id = project['repositories']['Github']

        token = self._userModel.get_user_githubToken()
        requester = GithubApiRequester(token)

        repos_commits = []
        for id in repositories_id:
            rp = requester.get_rp_by_id(id)
            if rp is not None:
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
        #print(all_repo_week_commit)
        return all_repo_week_commit

    def get_compare_week_commit(self, pid1, pid2):
        commit1 = self.get_weekcommit(pid1)
        if commit1 == {}:
            return {}
        commit1_info = {'pid' : pid1, 'commit' : commit1['commit_info']}
        commit2 = self.get_weekcommit(pid2)
        if commit2 == {}:
            return {}
        commit2_info = {'pid' : pid2, 'commit' : commit2['commit_info']}

        max = lambda m, n: m if m >= n else n
        min = lambda m, n: m if m <= n else n
        new_start_time = max(commit1['start_time'], commit2['start_time'])
        new_end_time = max(commit1['end_time'], commit2['end_time'])
        commit_info_list = [commit1_info, commit2_info]
        compare_repo_week_commit = dict({
            'commit_info' : commit_info_list,
            'start_time' : new_start_time,
            'end_time' : new_end_time
        })
        return compare_repo_week_commit


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

        week_dict['start_time'] = str(datetime.date(2099, 12, 31)).replace('-', '/')
        week_dict['end_time'] = str(datetime.date(1999, 1, 1)).replace('-', '/')
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
