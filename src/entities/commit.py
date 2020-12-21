class Commit():
    def __init__(self, author, message, lines, time):
        self.author = author
        self.message = message
        self.lines = lines
        self.time = time

    @staticmethod
    def from_dict(source):
        commit_msg = Commit(source[u'author'], source[u'message'], source[u'lines'], source[u'time'])

        if u'author' in source:
            commit_msg.author = source[u'author']
        if u'message' in source:
            commit_msg.message = source[u'message']
        if u'lines' in source:
            commit_msg.lines = source[u'lines']
        if u'time' in source:
            commit_msg.time = source[u'time']

        return commit_msg
    
    def to_dict(self):
        dest = {
            u'author': self.author,
            u'message': self.message,
            u'lines': self.lines,
            u'time': self.time
        }

        if self.author:
            dest[u'author'] = self.author
        if self.message:
            dest[u'message'] = self.message
        if self.lines:
            dest[u'lines'] = self.lines
        if self.time:
            dest[u'time'] = self.time
        
        return dest

    def __repr__(self):
        return (
            f'commit(\
                author={self.author}, \
                message={self.message}, \
                lines={self.lines}, \
                time={self.time}\
            )'
        )
    