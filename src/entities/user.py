class User():
    def __init__(self, name, email):

        self.name = name
        self.email = email
        self.github = None

    @staticmethod
    def from_dict(source):
        user = User(source['name'], source['email'])

        if u'name' in source:
            user.name = source['name']
        if u'email' in source:
            user.email = source['email']

        return user

    def to_dict(self):
        dest = {
            'name': self.name,
            'email': self.email,
            'Github': self.github
        }

        # if self.name:
        #     dest['name'] = self.name
        # if self.email:
        #     dest['email'] = self.email

        return dest

    def __repr__(self):
        return (
            f'user(\
                name={self.name}, \
                email={self.email} \
            )'
        )
