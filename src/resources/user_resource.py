from flask import jsonify, abort
from flask_restful import Resource
from common import error_code
from models.user_information_model import UserInformationModel

class UserResource(Resource):
    def get(self, uid=None):
        data = UserInformationModel.user_information(uid)
        if data == error_code.NO_SUCH_ELEMENT:
            abort(404)
        return jsonify(data)
        