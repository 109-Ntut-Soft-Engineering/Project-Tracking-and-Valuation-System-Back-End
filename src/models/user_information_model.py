from common import error_code
from db import Database

class UserInformationModel():
    @staticmethod
    def user_information(uid=None):
        db = Database('test_token').db

        if uid is None:
            users = db.collection(u'users').stream()
            return { 'users': user.to_dict() for user in users }
        else:
            users = db.collection(u'users').where(u'uid', u'==', uid).stream()
            if users is None:
                return error_code.NO_SUCH_ELEMENT
            return { 'user': user.to_dict() for user in users }