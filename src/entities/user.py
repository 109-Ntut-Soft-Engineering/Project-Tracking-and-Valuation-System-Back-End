class User():
    def __init__(self, name, email):
        self.name = name
        self.email = email

    @staticmethod
    def from_dict(source):
        user = User(source['name'], source['email'])

        return user

    def to_dict(self):
        dest = {
            'name': self.name,
            'email': self.email,
        }

        # if self.name:
        #     dest['name'] = self.name
        # if self.email:
        #     dest['email'] = self.email

        return dest
