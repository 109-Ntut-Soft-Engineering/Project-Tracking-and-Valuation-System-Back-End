from itertools import tee
from firebase_admin import auth
from flask_restful import abort
from functools import wraps
from flask import request
import traceback


def is_iter_empty(src_iter):
    it1, it2 = tee(src_iter)
    if next(it1, None) is None:
        return True, it2
    else:
        return False, it2


def verify_Idtoken(idToken):
    try:
        token = idToken.split(' ')[1]
        # print(token)
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token['uid']
        # print(uid)
        return uid
    except Exception as e:
        print(e)
        abort(401)


# def authenticate(func):
#     # @wraps(func)
#     def wrapper(arg):
#         print(func)
#         idToken = request.headers['Authorization']
#         uid= verify_Idtiken(idToken)

#         # if acct:
#         return func(uid)

#         # abort(401)
#     return wrapper
