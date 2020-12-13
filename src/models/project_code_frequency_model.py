from utilities.github_api_requester import GithubApiRequester
from conn_tool import ConnTool


class ProjectCodeFrequencyModel():
    def __init__(self, id_token):
        _conn_tool = ConnTool(id_token)
        self._db = _conn_tool.db
        self._uid = _conn_tool.uid

    def get_code_freq(self, name, token):
        project = self.__get_project(name)
        print('project:', project)
        repositories = self.__get_repositories(project)

        requester = GithubApiRequester(token)
        code_freqies= []
        for repository in repositories:
            # 用url拿到rp
            rp = requester.get_rp_by_rul(repository['url'])
            if rp is None:
                pass
            else:
                # get_stats_code_frequency 可以換成你要的
                # 先不要用get_rp_info 他會撈code_freq, issues, commits會有點久
                code_freq = requester.get_code_freq(rp)
                code_freqies.append(code_freq)

        code_freq_series = {}
        for rp_code_freq in code_freqies:
            for week_data in rp_code_freq:
                date = week_data['week']
                progress = week_data['additions'] - week_data['deletion']
                if date not in code_freq_series.keys():
                    code_freq_series[date] = progress
                else:
                    code_freq_series += progress
        date_code = []
        for date, code in code_freq_series.items():
            date_code.append({'date': date, 'code': code})
        return date_code

    def __get_project(self, name):
        project = self.__get_unique(self._db.collection(u'projects').where(u'name', u'==', name)).to_dict()
        return project

    def __get_repositories(self, project):
        repositories = []
        rids = map(int, project[u'repositories'])
        try:
            for rid in rids:
                repository = self.__get_unique(self._db.collection(u'repositories').where(u'rid', u'==', rid))
                repository = repository.to_dict()
                print('repository:', repository)
                repositories.append(repository)
        except :
                print("get repository occur error.")
        return repositories

    def __get_unique(self, collection):
        return next(collection.stream())

