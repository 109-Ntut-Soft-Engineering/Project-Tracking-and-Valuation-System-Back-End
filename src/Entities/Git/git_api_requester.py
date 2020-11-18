from github import Github
from github import Repository
from src.Entities.Git.git_object_parser import GitObjectParser


class GitApiRequester(object):
    def __init__(self, token):
        self.git = Github(token)
        self.parser = GitObjectParser()

    def search(self, name):
        rp = self.get_rp_by_name(name)

        rp_info = {}
        rp_info["name"] = rp.name
        rp_info["issues"] = self.parser.parser_issues(rp.get_issues())
        return rp_info

    def get_user(self):
        return self.git.get_user()

    def get_rp_by_name(self, name: str):
        return self.git.get_repo(name)
    #
    # def get_labels(self, issue):




if __name__ == '__main__':
    import json
    user = "s88037zz@gmail.com"
    password ='asd87306128'
    token = ' ef4164107b7e4e2505abd8fced70951f44e51964'
    requester = GitApiRequester(token)
    user = requester.get_user()
    print(user.name)

    # rp = requester.get_rp_by_name("s88037zz/just_buy")
    # for issue in rp.get_issues():
    #     print(issue)

    rp_info = requester.search("s88037zz/just_buy")
    result = json.dumps(rp_info, indent=1)
    print(result)
    # rp = requester.get_rp_by_url("https://github.com/s88037zz/just_buy_front_end")
    # print(rp)

