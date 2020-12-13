import gitlab
from utilities.requester import Requester


class GitlabApiRequester:
    def __init__(self, token):
        self.gitlab = gitlab.Gitlab('https://gitlab.com/', private_token=token)
        self.gitlab.auth()

    def get_repository_by_name(self, group_name, project_name):
        group = self.gitlab.groups.get(group_name)
        if group is None:
            print('Cant find', group_name)
            return None
        else:
            print('Find ', group.name)
            projects = group.projects.list(searc=project_name, all=True)
            print(' there are {} projects'.format(len(projects)))
            for project in projects:
                if project.path_with_namespace == group_name+'/'+project_name:
                    return project
            return None

    def get_repository_by_url(self, url):
        'https://gitlab.com/s88037zz/soft-engineering-front-end.git'
        if 'https://gitlab.com/' in url:
            url = url.replace('https://gitlab.com/', '').replace('.git', '')
            group_name, project_name = url.split('/')
            print('gp_name, pro_name:', group_name, project_name)
            return self.get_repository_by_name(group_name, project_name)
        else:
            raise ValueError('Url is not from gitlab source.')


    def get_commits(self, rp):
        return self.gitlab.projects.get(rp.id, lazy=True).commits.list()

    def get_issues(self, rp):
        return self.gitlab.projects.get(rp.id, lazy=True).issues.list()

    def get_code_freq(self, rp):
        return

if __name__ == '__main__':
    token = 'eijr9MQx7NCzwSnGfBFK'
    gitlab = GitlabApiRequester(token)
    url = 'https://gitlab.com/ase/ase.git'

    # search by url
    project = gitlab.get_repository_by_url(url)
    print(type(project))
    print(project.id)

    commits = gitlab.get_commits(project)
    for index, commit in enumerate(commits):
        print('Idx: {}, commit:{}'.format(index, commit.title))

    issues = gitlab.get_issues(project)
    for index, issue in enumerate(issues):
        print('Idx: {}, issue:{}'.format(index, issue.title))