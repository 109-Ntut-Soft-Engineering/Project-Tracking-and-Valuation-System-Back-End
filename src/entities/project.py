from entities.entity import Entity

class Project(Entity):
    def __init__(self, pid, name, owner, repositories):
        self.pid = pid
        self.name = name
        self.owner = owner
        self.repositories = repositories

    @staticmethod
    def from_dict(source):
        project = Project(source[u'pid'], source[u'name'], source[u'owner'], source[u'repositories'])

        if u'pid' in source:
            project.name = source[u'pid']
        if u'name' in source:
            project.name = source[u'name']
        if u'owner' in source:
            project.owner = source[u'owner']
        if u'repositories' in source:
            project.repositories = source[u'repositories']

        return project
    
    def to_dict(self):
        dest = {
            u'pid':self.pid, 
            u'name':self.name, 
            u'owner':self.owner, 
            u'repositories':self.repositories
        }

        if self.pid:
            dest[u'pid'] = self.pid
        if self.name:
            dest[u'name'] = self.name
        if self.owner:
            dest[u'owner'] = self.owner
        if self.repositories:
            dest[u'repositories'] = self.repositories
        
        return dest

    def __repr__(self):
        return (
            f'project(\
                pid={self.pid}, \
                name={self.name}, \
                owner={self.owner}, \
                repositories={self.repositories}\
            )'
        )
    