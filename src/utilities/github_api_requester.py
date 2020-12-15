from github import Github
from github import Repository
from github import AuthenticatedUser
from utilities.github_object_parser import GithubObjectParser
from utilities.requester import Requester

# from github_object_parser import GithubObjectParser
# from requester import Requester


class GithubApiRequester(Requester):
    def __init__(self, token):
        self.github = Github(token)

    def search(self, name):
        return self.get_rp_by_id(name)

    def get_rp_info(self, rp):

        rp_info = {}
        rp_info["name"] = rp.name

        # deal with issues
        rp_info["issues"] = self.get_issues(rp)

        # deal with code frequeny
        rp_info["code_freq"] = self.get_code_freq(rp)

        # deal with commits
        rp_info['commits'] = self.get_commits(rp)
        return rp_info

    def get_user_repoList(self):
        starred = self.github.get_user().get_starred()
        repos = self.github.get_user().get_repos()
        return GithubObjectParser.parser_repo_list([repos, starred])



    def get_user(self) -> AuthenticatedUser:
        return self.github.get_user()

    def get_rp_by_id(self, id) -> Repository:
        try:
            return self.github.get_repo(id)
        except Exception:
            print("Can't find {} from github".format(id))
            return None

    def get_rp_by_rul(self, url: str) -> Repository:
        try:
            name = self.__parse_url(url)
            return self.get_rp_by_id(name)
        except Exception as e:
            print("e")
            return None

    def get_issues(self, rp):
        issues = rp.get_issues()
        return GithubObjectParser.parser_issues(issues)

    def get_code_freq(self, rp) -> list:
        stats_code_frequency = rp.get_stats_code_frequency()
        return GithubObjectParser.parser_stats_code_frequencies(stats_code_frequency)

    def get_commits(self, rp):
        commits = rp.get_commits()
        return GithubObjectParser.parser_commits(commits)

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
    token = '9cef1886c6974e6d20323cdbdace6c5da9377d2c'
    requester = GithubApiRequester(token)

    print(requester.get_user_starredList().totalCount)
