class Repo():
    def __init__(self, rid, name, url):
        self.rid = rid
        self.name = name
        self.url = url

    @staticmethod
    def from_dict(source):
        repo = Repo(source[u'rid'], source[u'name'], source[u'url'])

        if u'rid' in source:
            repo.rid = source[u'rid']
        if u'name' in source:
            repo.name = source[u'name']
        if u'url' in source:
            repo.url = source[u'url']

        return repo

    def to_dict(self):
        dest = {
            u'rid':self.rid, 
            u'name':self.name,
            u'url':self.url
        }

        if self.rid:
            dest[u'rid'] = self.rid
        if self.name:
            dest[u'name'] = self.name
        if self.url:
            dest[u'url'] = self.url

        return dest

    def __repr__(self):
        return (
            f'repo(\
                rid={self.rid}, \
                name={self.name}, \
                url={self.url}\
            )'
        )
