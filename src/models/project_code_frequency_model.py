from utilities.github_api_requester import GithubApiRequester
from conn_tool import ConnTool
from models.user_model import UserModel
from datetime import datetime


class ProjectCodeFrequencyModel:
    def __init__(self):
        _conn_tool = ConnTool()
        self._db = _conn_tool.db
        self._uid = _conn_tool.uid
        self._userModel = UserModel()

    def get_code_freq(self, pid):
        project = self.__get_project(pid)
        repositories_id = project['repositories']['Github']
        print('repositories:', repositories_id)

        token = self._userModel.get_user_githubToken()

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

        date_code = self.__sort_code_freq(date_code)
        date_code = self.__delete_post_zero(date_code)
        return date_code

    def __sort_code_freq(self, code_freq):
        dateFormatter = '%Y/%m/%d'
        code_freq = sorted(code_freq, key=lambda data: datetime.strptime(data['date'], dateFormatter))
        print("sorted", code_freq)
        return code_freq

    def __delete_post_zero(self, code_freq):
        for i in range(len(code_freq)-1, 0, -1):
            print("code[i]:", code_freq[i]['code'])
            if code_freq[i]['code'] != 0:
                return code_freq[0:i]
        return code_freq[0:]

    def __get_project(self, pid):
        project = self._db.collection(
            u'projects').document(pid).get().to_dict()

        return project

    def __get_unique(self, collection):
        return next(collection.stream())


