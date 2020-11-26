from common import error_code
from db import Database

class ProjectAndRepositoryModel():
    @staticmethod
    def project_information(pid=None):
        database = Database('test_token')
        db = database.db
        uid = database.uid

        if pid is None:
            docs = db.collection(u'projects').where(u'owner', u'array_contains', uid).stream()
            return { 'projects': doc.to_dict() for doc in docs }
        else:
            docs = db.collection(u'projects').where(u'pid', u'==', pid).stream()
            if docs is None:
                return error_code.NO_SUCH_ELEMENT
            return { 'project': doc.to_dict() for doc in docs }