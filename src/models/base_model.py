class BaseModel():
    def __init__(self, db, uid):
        self._db = db
        self._uid = uid

    @property
    def db(self):
        return self._db

    @property
    def uid(self):
        return self._uid