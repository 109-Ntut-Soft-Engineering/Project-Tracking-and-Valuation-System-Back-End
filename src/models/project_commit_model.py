from conn_tool import ConnTool
from utilities.github_api_requester import GithubApiRequester
from entities.commit import Commit
from entities.commits import Commits
from datetime import datetime
import sys


class ProjectCommitModel():
    def __init__(self):
        _conn_tool = ConnTool()
        self._db = _conn_tool.db
        self._uid = _conn_tool.uid

    def get_project_commit_info(self, pid):
        project = self._db.collection(u'projects').document(pid).get().to_dict()
        commits = self.__get_commits(project)
        print(commits, file=sys.stderr)
        return {"commits": commits.to_dict()}

    def __get_commits(self, project):
        repositories = project['repositories']['Github']
        print(repositories, file=sys.stderr)

        token = ' ef4164107b7e4e2505abd8fced70951f44e51964'
        requester = GithubApiRequester(token)

        commit_messages = []
        for repository in repositories:
            src_commits = requester.get_commits(
                requester.get_rp_by_id(repository))
            for src_commit in src_commits:
                dest_commit = self.__transform_commit(src_commit)
                commit_messages.append(dest_commit)

        commits = self.__build_commits(project[u'name'], commit_messages)
        self.sort_commits_by_time(commits, 'desc')
        return commits

    def __transform_commit(self, src_commit):
        name = src_commit['commit']['author']['name']
        message = src_commit['commit']['message']
        lines = src_commit['stats']['total']
        time = src_commit['commit']['author']['date'].split(',')[0]
        dest_commit = Commit(name, message, lines, time)
        return dest_commit

    def __build_commits(self, project_name, commit_messages):
        member = [commit.user_name for commit in commit_messages]
        member = list(set(member))
        commits = Commits(project_name, member, commit_messages)
        return commits

    def sort_commits_by_time(self, commit_msgs, sort_type):
        if sort_type == 'desc':
            commit_msgs.sort(key=lambda x: 
                datetime.strip(x['time'], '%y/%m/%d'), reversed=False)
        elif sort_type == 'asc':
            commit_msgs.sort(key=lambda x: 
                datetime.strip(x['time'], '%y/%m/%d'), reversed=True)
        else:
            exit('sort type only have "desc" & "asc"')

