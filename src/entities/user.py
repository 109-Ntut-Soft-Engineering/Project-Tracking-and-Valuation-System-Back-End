class User():
    def __init__(self, uid, name, email):
        self.uid = uid
        self.name = name
        self.email = email

    @staticmethod
    def from_dict(source):
        user = User(source[u'uid'], source[u'name'], source[u'email'])

        if u'uid' in source:
            user.uid = source[u'uid']
        if u'name' in source:
            user.name = source[u'name']
        if u'email' in source:
            user.email = source[u'email']

        return user

    def to_dict(self):
        dest = {
            u'uid':self.uid, 
            u'name':self.name,
            u'email':self.email
        }

        if self.uid:
            dest[u'uid'] = self.uid
        if self.name:
            dest[u'name'] = self.name
        if self.email:
            dest[u'email'] = self.email


        return dest

    def __repr__(self):
        return (
            f'user(\
                uid={self.uid}, \
                name={self.name}, \
                email={self.email} \
            )'
        )
