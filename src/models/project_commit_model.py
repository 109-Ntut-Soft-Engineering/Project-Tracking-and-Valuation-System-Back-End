from utilities.github_api_requester import GithubApiRequester
from entities.commit import Commit
from entities.commits import Commits
from datetime import datetime
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

        msg = {
            pid1: commits1['commits'], 
            pid2: commits2['commits']
        }

        return msg

    def get_project_commit(self, pid):
        project = self._db.collection(
            u'projects').document(pid).get().to_dict()
        commits = self.__get_commits(project)
        return {"commits": commits.to_dict()}

    def __get_commits(self, project):
        repositories = project['repositories']['Github']

        requester = GithubApiRequester(self._token(project['owner']))

        commit_list = []
        for repository in repositories:
            src_commits = requester.get_commits(
                requester.get_rp_by_id(repository))
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
