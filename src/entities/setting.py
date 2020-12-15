class Setting():
    def __init__(self, name, owner, collaborator):
        self.name = name
        self.owner = owner
        self.collaborator = collaborator

    def to_dict(self):
        dest = {
            u'name':self.name, 
            u'owner':self.owner,
            u'collaborator':self.collaborator
        }

        return dest