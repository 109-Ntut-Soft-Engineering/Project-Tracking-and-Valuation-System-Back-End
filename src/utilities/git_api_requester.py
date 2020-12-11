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
        return self.get_rp_by_id(name)

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
        return GitObjectParser.parser_repo_list(self.git.get_user().get_repos())

    def get_user(self) -> AuthenticatedUser:
        return self.git.get_user()

    def get_rp_by_id(self, id: str) -> Repository:
        try:
            return self.git.get_repo(id)
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
    token = '445d5e39b2d3f4abc9c0063fe3ff1f689470c3c5'
    requester = GitApiRequester(token)
    # repos = requester.get_repoList()
    # print(repos)

    # rp = requester.get_rp_by_name(
    #     "wei02427/DatabaseFrontend")
    # print(rp)
    # rp_info = requester.get_rp_info(rp)
    # print(json.dumps(rp_info, indent=1))

    print(GitObjectParser.parser_repo_list(requester.get_repoList()))
