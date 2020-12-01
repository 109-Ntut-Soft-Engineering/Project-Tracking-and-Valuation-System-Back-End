from flask import jsonify, abort
from flask_restful import Resource
from resources.base_resource import BaseResource
from common import error_code
from common.util import is_iter_empty

class UserResource(BaseResource):
    def get(self, uid=None):
        data = self.__user_information(uid)
        if data == error_code.NO_SUCH_ELEMENT:
            abort(404)
        return jsonify(data)
        
    def __user_information(self, uid=None):
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
