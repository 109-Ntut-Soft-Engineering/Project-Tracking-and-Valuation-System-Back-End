class Project():
    def __init__(self, name, owner, repositories=None):

        self.name = name
        self.owner = owner
        self.repositories = repositories

    @staticmethod
    def from_dict(source):
        project = Project(
            source[u'name'], source[u'owner'], source[u'repositories'])

        # if u'name' in source:
        #     project.name = source[u'name']
        # if u'owner' in source:
        #     project.owner = source[u'owner']
        # if u'repositories' in source:
        #     project.repositories = source[u'repositories']

        return project

    def to_dict(self):
        dest = {
            'name': self.name,
            'owner': self.owner,
            'repositories': self.repositories
        }

        # if self.pid:
        #     dest['pid'] = self.pid
        # if self.name:
        #     dest['name'] = self.name
        # if self.owner:
        #     dest['owner'] = self.owner
        # if self.repositories:
        #     dest['repositories'] = self.repositories

        return dest

    def __repr__(self):
        return (
            f'project(\
                name={self.name}, \
                owner={self.owner}, \
                repositories={self.repositories}\
            )'
        )
