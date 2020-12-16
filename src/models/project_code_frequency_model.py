from utilities.github_api_requester import GithubApiRequester
from conn_tool import ConnTool


class ProjectCodeFrequencyModel:
    def __init__(self):
        _conn_tool = ConnTool()
        self._db = _conn_tool.db
        self._uid = _conn_tool.uid

    def get_code_freq(self, pid):
        project = self.__get_project(pid)
        repositories_id = project['repositories']['Github']
        print('repositories:', repositories_id)

        token = ' ef4164107b7e4e2505abd8fced70951f44e51964'
        requester = GithubApiRequester(token)
        code_freqies = []
        for id in repositories_id:
            # 用url拿到rp
            print('id:', id)
            rp = requester.get_rp_by_id(id)
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
                    code_freq_series[date] += progress
        date_code = []
        for date, code in code_freq_series.items():
            date_code.append({'date': date, 'code': code})
        return date_code


    def __get_project(self, pid):
        project = self._db.collection(u'projects').document(pid).get().to_dict()

        return project

    def __get_unique(self, collection):
        return next(collection.stream())
