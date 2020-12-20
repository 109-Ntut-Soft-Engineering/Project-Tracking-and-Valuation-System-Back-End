from github import Github
from github import Repository
from github import AuthenticatedUser
from utilities.github_object_parser import GithubObjectParser
from utilities.requester import Requester


class GithubApiRequester(Requester):
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
        rp_info["code_freq"] = self.get_code_freq(rp)

        # deal with commits
        rp_info['commits'] = self.get_commits(rp)
        return rp_info

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
        return GithubObjectParser.parser_issues(issues)

    def get_weekcommit(self, rp):
        commits = rp.get_commits()
        return GithubObjectParser.parser_weekcommit(commits)

    def get_code_freq(self, rp) -> list:
        stats_code_frequency = rp.get_code_freq()
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
    password ='asd87306128'
    token = ' ef4164107b7e4e2505abd8fced70951f44e51964'
    requester = GithubApiRequester(token)
    user = requester.get_user()
    print(user.name)

    rp = requester.get_rp_by_name("Gougon-Side-Project/Android-DodoCagePhonograph")
    rp_info = requester.get_rp_info(rp)
    print(json.dumps(rp_info, indent=1))


