from utilities.github_api_requester import GithubApiRequester
from entities.commit import Commit
from entities.commits import Commits
from entities.my_date import MyDate
from datetime import datetime, timedelta
from models.user_model import UserModel
import sys


class ProjectCommitModel():
    def __init__(self, conn_tool):
        self._db = conn_tool.db
        self._uid = conn_tool.uid
        self._token = UserModel(conn_tool).get_user_githubToken

    def get_compare_project_commit(self, pid1, pid2):
        commits1 = self.get_project_commit(pid1)
        commits2 = self.get_project_commit(pid2)

        cmt_times1_list = self.__get_commit_times(commits1)
        cmt_times2_list = self.__get_commit_times(commits2)

        start_date = None
        end_date = None
        if MyDate(date_text=cmt_times1_list[0]['time']).smaller_than(
            MyDate(date_text=cmt_times2_list[0]['time'])):
            start_date = MyDate(date_text=cmt_times1_list[0]['time'])
        else:
            start_date = MyDate(date_text=cmt_times2_list[0]['time'])

        if MyDate(date_text=cmt_times1_list[-1]['time']).smaller_than(
            MyDate(date_text=cmt_times2_list[-1]['time'])):
            end_date = MyDate(date_text=cmt_times2_list[-1]['time'])
        else:
            end_date = MyDate(date_text=cmt_times1_list[-1]['time'])

        cmt_times1_list = self.__fill_empty_date(cmt_times1_list, start_date, end_date)
        cmt_times2_list = self.__fill_empty_date(cmt_times2_list, start_date, end_date)

        print(cmt_times1_list, file=sys.stderr)
        msg = {
            'commit_times': [
                { 'time': cmt_times1['time'], 
                  str(pid1): cmt_times1['times'], 
                  str(pid2): cmt_times2['times'] 
                } for cmt_times1, cmt_times2 in \
                    zip(cmt_times1_list, cmt_times2_list)
            ]
        }

        return msg

    def __get_commit_times(self, commits):
        print(commits, file=sys.stderr)
        commits = commits['commits']['commit_list']
        cmt_times_list = []
        cmt_times = {
            'times': 1, 
            'time': commits[0]['time']
        }
        cmt_times_list.append(cmt_times)
        for idx in range(1, len(commits)):
            if commits[idx]['time'] == cmt_times_list[-1]['time']:
                cmt_times_list[-1]['times'] += 1
            else:
                cmt_times = {
                    'times': 1, 
                    'time': commits[idx]['time']
                }
                start_date = MyDate(date_text=cmt_times_list[-1]['time'])
                end_date = MyDate(date_text=cmt_times['time'])
                interval_dates = self.__get_interval_commit_times(start_date, end_date)
                cmt_times_list += interval_dates
                cmt_times_list.append(cmt_times)
        return cmt_times_list

    def __get_interval_commit_times(self, start_date, end_date, involve_s=False, involve_e=False):
        interval_dates = []
        if not involve_s:
            start_date.next_day()
        while start_date.smaller_than(end_date):
            interval_dates.append({
                'times': 0, 
                'time': start_date.date_text
            })
            start_date.next_day()
        if involve_e:
            interval_dates.append({
                'times': 0, 
                'time': end_date.date_text
            })
        return interval_dates

    def __fill_empty_date(self, cmt_times, start_date, end_date):
        print('a', file=sys.stderr)
        if start_date.smaller_than(MyDate(date_text=cmt_times[0]['time'])):
            print('b', file=sys.stderr)
            begin_dates = (self.__get_interval_commit_times(
                start_date, MyDate(date_text=cmt_times[0]['time']), involve_s=True))
            cmt_times = begin_dates + cmt_times
        if MyDate(date_text=cmt_times[-1]['time']).smaller_than(end_date):
            print('c', file=sys.stderr)
            end_dates = self.__get_interval_commit_times(
                MyDate(date_text=cmt_times[-1]['time']), end_date, involve_e=True)
            cmt_times = cmt_times + end_dates
        return cmt_times

    def get_project_commit(self, pid):
        project = self._db.collection(
            u'projects').document(pid).get().to_dict()
        commits = self.__get_commits(project)
        return {"commits": commits.to_dict()}

    def __get_commits(self, project):
        repositories = project['repositories']['Github']

        requester = GithubApiRequester(self._token(project['owner']))

        commit_list = []
        print('before loop', file=sys.stderr)
        print(repositories, file=sys.stderr)
        for repository in repositories:
            print('in loop', file=sys.stderr)
            print(repository, file=sys.stderr)
            rp = requester.get_rp_by_id(repository)
            print(rp, file=sys.stderr)
            src_commits = requester.get_commits(rp)
            for src_commit in src_commits:
                dest_commit = self.__transform_commit(src_commit)
                commit_list.append(dest_commit)

        commits = self.__build_commits(project[u'name'], commit_list)
        self.__sort_commits_by_time(commits, 'asc')
        return commits

    def __transform_commit(self, src_commit):
        print(src_commit, file=sys.stderr)
        name = src_commit['commit']['author']['name']
        message = src_commit['commit']['message']
        lines = src_commit['stats']['total']
        time = src_commit['commit']['author']['date'].split(',')[0]
        dest_commit = Commit(name, message, lines, time)
        return dest_commit

    def __build_commits(self, project_name, commit_list):
        member = [commit.author for commit in commit_list]
        member = list(set(member))
        commits = Commits(project_name, member, commit_list)
        return commits

    def __sort_commits_by_time(self, commits, sort_type):
        commit_list = commits.commit_list
        if sort_type == 'asc':
            commit_list.sort(key=lambda x:
                             datetime.strptime(x.time, '%Y/%m/%d'), reverse=False)
        elif sort_type == 'desc':
            commit_list.sort(key=lambda x:
                             datetime.strptime(x.time, '%Y/%m/%d'), reverse=True)
        else:
            exit('sort type only have "desc" & "asc"')
