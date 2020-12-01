class Repository:
    def __init__(self, pid, name, commits, issues, code_feq, token):
        self.pid = pid
        self.name = name 
        self.commits = commits
        self.issues = issues
        self.code_freq = code_feq
        self.token = token

    @staticmethod
    def from_dict(source):
        repository = Repository(source[u'pid'],
                                source[u'name'],
                                source[u'commits'],
                                source[u'issues'],
                                source[u'code_freq'],
                                source[u'token'])

        return repository

    def to_dict(self):
        repository = {
            u'pid': self.pid,
            u'name': self.name,
            u'commits': self.commits,
            u'issues': self.issues,
            u'code_feq': self.code_freq,
            u'token': self.token
        }
        return repository