from github import Github
from github import Repository
from github import AuthenticatedUser
from utilities.git_object_parser import GitObjectParser
# from git_object_parser import GitObjectParser
from firebase_admin import auth


class GitApiRequester(object):
    def __init__(self, token):
        self.git = Github(token)

    def search(self, name):
        return self.get_rp_by_name(name)

    def get_rp_info(self, rp):

        rp_info = {}
        rp_info["name"] = rp.name

        # deal with issues
        rp_info["issues"] = self.get_issues(rp)

        # deal with code frequeny
        rp_info["code_freq"] = self.get_stats_code_frequency(rp)

        # deal with commits
        rp_info['commits'] = self.get_commits(rp)
        return rp_info

    def get_repoList(self):
        return self.git.get_user().get_repos()

    def get_user(self) -> AuthenticatedUser:
        return self.git.get_user()

    def get_rp_by_name(self, name: str) -> Repository:
        try:
            return self.git.get_repo(name)
        except Exception:
            print("Can't find {} from github".format(name))
            return None

    def get_rp_by_rul(self, url: str) -> Repository:
        try:
            name = self.__parse_url(url)
            return self.get_rp_by_name(name)
        except Exception as e:
            print("e")
            return None

    def get_issues(self, rp):
        issues = rp.get_issues()
        return GitObjectParser.parser_issues(issues)

    def get_stats_code_frequency(self, rp) -> list:
        stats_code_frequency = rp.get_stats_code_frequency()
        return GitObjectParser.parser_stats_code_frequencies(stats_code_frequency)

    def get_commits(self, rp):
        commits = rp.get_commits()
        return GitObjectParser.parser_commits(commits)

    def __parse_url(self, url):
        print('url', url)
        if "github.com" not in url:
            raise ValueError("repository url is not valid")
        else:
            name = url.replace('https://github.com/', "")
            return name


if __name__ == '__main__':
    import json
    user = "s88037zz@gmail.com"
    password = 'asd87306128'
    token = '6f013b3f8aaa5876602f9f0c2b575551ca9c2d6d'
    requester = GitApiRequester(token)
    user = requester.get_user()
    print(user)

    # rp = requester.get_rp_by_name(
    #     "wei02427/DatabaseFrontend")
    # print(rp)
    # rp_info = requester.get_rp_info(rp)
    # print(json.dumps(rp_info, indent=1))

    # for repo in (requester.get_repoList()):
    #     print(repo)
