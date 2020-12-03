from models.base_model import BaseModel
from entities.user import User
from common import status_code, error_code
from common.status_code import is_client_error
from common.util import is_iter_empty

class UserModel(BaseModel):
    def get_user_information(self, uid=None):
        if uid is None:
            users = self.db.collection(u'users').stream()
            return { 'users': user.to_dict() for user in users }
        else:
            users = self.db.collection(u'users').where(u'uid', u'==', uid).stream()
            is_empty, users = is_iter_empty(users)
            if is_empty:
                return error_code.NO_SUCH_ELEMENT
            users = self.db.collection(u'users').where(u'uid', u'==', uid).stream()
            return { 'user': user.to_dict() for user in users }

    def add_user(self, name, email):
        if self.__is_uid_exist(self.uid) or self.__is_email_exist(self.uid):
            return status_code.BAD_REQUEST

        user = User(uid=self.uid, name=name, email=email)

        self.db.collection(u'users').document().set(user.to_dict())

        return status_code.OK

    def __is_uid_exist(self, uid):
        users = self.db.collection(u'users').where(u'uid', u'==', self.uid).stream()
        return not is_iter_empty(users)[0]

    def __is_email_exist(self, email):
        users = self.db.collection(u'users').where(u'email', u'==', email).stream()
        return not is_iter_empty(users)[0]
