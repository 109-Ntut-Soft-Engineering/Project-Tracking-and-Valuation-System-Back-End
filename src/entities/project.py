class Project():
    def __init__(self, name, owner, collaborator=[], repositories={'Github': []}, updated=None):
        self.name = name
        self.owner = owner
        self.collaborator = collaborator
        self.repositories = repositories
        self.updated = updated

    @staticmethod
    def from_dict(source):
        project = Project(
            source[u'name'], 
            source[u'owner'], 
            source[u'collaborator'], 
            source[u'repositories'], 
            source[u'updated']
        )

        return project

    def to_dict(self):

        dest = {}

        if self.name:
            dest['name'] = self.name
        if self.owner:
            dest['owner'] = self.owner
        if self.owner:
            dest['collaborator'] = self.collaborator
        if self.repositories:
            dest['repositories'] = self.repositories
        if self.updated:
            dest['updated'] = self.updated.__str__()

        return dest
