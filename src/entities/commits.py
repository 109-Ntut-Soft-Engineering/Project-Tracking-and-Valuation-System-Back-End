class Commits():
    def __init__(self, name, member, commit_messages):
        self.name = name
        self.member = member
        self.commit_messages = commit_messages

    @staticmethod
    def from_dict(source):
        commit = Commits(source[u'name'], source[u'member'], source[u'commit_messages'])

        if u'name' in source:
            commit.name = source[u'name']
        if u'member' in source:
            commit.member = source[u'member']
        if u'commit_messages' in source:
            commit.commit_messages = source[u'commit_messages']

        return commit
    
    def to_dict(self):
        dest = {
            u'name': self.name,
            u'member': self.member,
            u'commit_messages': [commit.to_dict() for commit in self.commit_messages]
        }

        if self.name:
            dest[u'name'] = self.name
        if self.member:
            dest[u'member'] = self.member
        if self.commit_messages:
            dest[u'commit_messages'] = [commit.to_dict() for commit in self.commit_messages]
        
        return dest

    def __repr__(self):
        return (
            f'project(\
                name={self.name}, \
                member={self.member}, \
                commit_messages={self.commit_messages}\
            )'
        )
    