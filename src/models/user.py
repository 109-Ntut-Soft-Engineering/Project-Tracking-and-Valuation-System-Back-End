class User():
    def __init__(self, uid, name):
        self.uid = uid
        self.name = name

    @staticmethod
    def from_dict(source):
        user = User(source[u'uid'], source[u'name'])

        if u'uid' in source:
            user.uid = source[u'uid']
        if u'name' in source:
            user.name = source[u'name']

        return user

    def to_dict(self):
        dest = {
            u'uid':self.uid, 
            u'name':self.name
        }

        if self.uid:
            dest[u'uid'] = self.uid
        if self.name:
            dest[u'name'] = self.name

        return dest

    def __repr__(self):
        return (
            f'user(\
                uid={self.uid}, \
                name={self.name}\
            )'
        )
