from models.base_model import BaseModel
from utilities.git_api_requester import GitApiRequester
from entities.commit import Commit
from entities.commits import Commits
import sys


class ProjectCommitModel(BaseModel):
    def get_project_commit_info(self, name):
        project = self.__get_unique(self.db.collection(
            u'projects').where(u'name', u'==', name)).to_dict()
        commits = self.__get_commits(project)
        print(commits, file=sys.stderr)
        return {"commits": commits.to_dict()}

    def __get_repositories(self, project):
        repositories = []
        rids = map(int, project[u'repositories'])
        for rid in rids:
            repository = self.__get_unique(self.db.collection(
                u'repositories').where(u'rid', u'==', rid))
            repository = repository.to_dict()
            repositories.append(repository)
        return repositories

    def __get_commits(self, project):
        repositories = self.__get_repositories(project)

        user = "s88037zz@gmail.com"
        password = 'asd87306128'
        token = ' ef4164107b7e4e2505abd8fced70951f44e51964'
        requester = GitApiRequester(token)

        commit_messages = []
        for repository in repositories:
            src_commits = requester.get_commits(
                requester.get_rp_by_id(repository['name']))
            for src_commit in src_commits:
                dest_commit = self.__transform_commit(src_commit)
                commit_messages.append(dest_commit)

        commits = self.__build_commits(project[u'name'], commit_messages)
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

    def __get_unique(self, collection):
        return next(collection.stream())
