from models.user_model import UserModel


class Setting():
    def __init__(self, name, collaborator, userModel):
        self.name = name
        self.collaborator = collaborator
        self.__userModel = userModel

    def to_dict(self):
        dest = {
            'name': self.name,
            'collaborator': [self.__userModel.get_user_info_by_uid(collab)[0] for collab in self.collaborator]
        }
        return dest
