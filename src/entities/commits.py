class Commits():
    def __init__(self, name, member, commit_list):
        self.name = name
        self.member = member
        self.commit_list = commit_list

    @staticmethod
    def from_dict(source):
        commit = Commits(source[u'name'], source[u'member'], source[u'commit_list'])

        if u'name' in source:
            commit.name = source[u'name']
        if u'member' in source:
            commit.member = source[u'member']
        if u'commit_list' in source:
            commit.commit_list = source[u'commit_list']

        return commit
    
    def to_dict(self):
        dest = {
            u'name': self.name,
            u'member': self.member,
            u'commit_list': [commit.to_dict() for commit in self.commit_list]
        }

        if self.name:
            dest[u'name'] = self.name
        if self.member:
            dest[u'member'] = self.member
        if self.commit_list:
            dest[u'commit_list'] = [commit.to_dict() for commit in self.commit_list]
        
        return dest

    def __repr__(self):
        return (
            f'project(\
                name={self.name}, \
                member={self.member}, \
                commit_list={self.commit_list}\
            )'
        )
    