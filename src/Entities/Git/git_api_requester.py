from github import Github
from github import Repository
from github import AuthenticatedUser
from src.Entities.Git.git_object_parser import GitObjectParser


class GitApiRequester(object):
    def __init__(self, token):
        self.git = Github(token)
        self.parser = GitObjectParser()

    def search(self, name):
         return self.get_rp_by_name(name)

    def get_rp_info(self, rp):
        rp_info = {}
        rp_info["name"] = rp.name

        # deal with issues
        issues = rp.get_issues()
        rp_info["issues"] = self.parser.parser_issues(issues)

        # deal with code frequeny
        stats_code_frequency = self.get_stats_code_frequency(rp)
        rp_info["stats_code_frequency"] = GitObjectParser.parser_stats_code_frequencies(stats_code_frequency)

        # deal with commits
        commits = self.get_commits(rp)
        rp_info['commits'] = GitObjectParser.parser_commits(commits[0:5])
        return rp_info

    def get_user(self) -> AuthenticatedUser:
        return self.git.get_user()

    def get_rp_by_name(self, name: str) -> Repository:
        return self.git.get_repo(name)

    def get_stats_code_frequency(self, rp) -> list:
        return rp.get_stats_code_frequency()

    def get_commits(self, rp):
        return rp.get_commits()


if __name__ == '__main__':
    import json
    user = "s88037zz@gmail.com  "
    password ='asd87306128'
    token = ' ef4164107b7e4e2505abd8fced70951f44e51964'
    requester = GitApiRequester(token)
    user = requester.get_user()
    print(user.name)

    rp = requester.get_rp_by_name("automl/auto-sklearn")
    rp_info = requester.get_rp_info(rp)
    print(json.dumps(rp_info, indent=1))


