class Commit():
    def __init__(self, user_name, message, lines, time):
        self.user_name = user_name
        self.message = message
        self.lines = lines
        self.time = time

    @staticmethod
    def from_dict(source):
        commit_msg = Commit(source[u'user_name'], source[u'message'], source[u'lines'], source[u'time'])

        if u'user_name' in source:
            commit_msg.user_name = source[u'user_name']
        if u'message' in source:
            commit_msg.message = source[u'message']
        if u'lines' in source:
            commit_msg.lines = source[u'lines']
        if u'time' in source:
            commit_msg.time = source[u'time']

        return commit_msg
    
    def to_dict(self):
        dest = {
            u'user_name': self.user_name,
            u'message': self.message,
            u'lines': self.lines,
            u'time': self.time
        }

        if self.user_name:
            dest[u'user_name'] = self.user_name
        if self.message:
            dest[u'message'] = self.message
        if self.lines:
            dest[u'lines'] = self.lines
        if self.time:
            dest[u'time'] = self.time
        
        return dest

    def __repr__(self):
        return (
            f'project(\
                pid={self.user_name}, \
                name={self.message}, \
                owner={self.lines}, \
                repositories={self.time}\
            )'
        )
    