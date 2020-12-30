from utilities.github_api_requester import GithubApiRequester
from conn_tool import ConnTool
from models.user_model import UserModel
from datetime import datetime


class ProjectCodeFrequencyModel:
    def __init__(self, connect_tool):
        self._db = connect_tool.db
        self._uid = connect_tool.uid
        self._token = UserModel(connect_tool).get_user_githubToken()

    def get_code_freq(self, pid):
        # 從第三方拿取資料
        code_freq_series = self.__get_code_freq_from_third(pid)
        date_code = []
        for date, code in code_freq_series.items():
            date_code.append({'date': date, 'code': code})

        date_code = self.__sort_code_freq(date_code)
        date_code = self.__delete_post_zero(date_code)
        return date_code

    def get_compare_code_frequency(self, pid1, pid2):
        pid1_code_freqies = self.get_code_freq(pid1)
        pid2_code_freqies = self.get_code_freq(pid2)

        compare_code_freies = {}
        for data in pid1_code_freqies:
            date = data['date']
            compare_code_freies[date]= {pid1: data['code'], pid2: 0}

        for data in pid2_code_freqies:
            date = data['date']
            if date in compare_code_freies.keys():
                compare_code_freies[date][pid2] = data['code']
            else:
                compare_code_freies[date] = {pid1: 0, pid2: data['code']}

        # redefine the structure
        date_code = []
        for date, data in compare_code_freies.items():
            date_code.append({'date': date, pid1: data[pid1], pid2: data[pid2]})

        print('compare date code:', date_code)
        return self.__sort_code_freq(date_code)




    def __get_code_freq_from_third(self, pid: str) -> dict:
        project = self.__get_project(pid)
        repositories_id = project['repositories']['Github']
        print('repositories:', repositories_id)
        token = self._token

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
        return code_freq_series

    def __sort_code_freq(self, code_freq):
        dateFormatter = '%Y/%m/%d'
        code_freq = sorted(code_freq, key=lambda data: datetime.strptime(data['date'], dateFormatter))
        print("sorted", code_freq)
        return code_freq

    def __delete_post_zero(self, code_freq):
        for i in range(len(code_freq)-1, 0, -1):
            if code_freq[i]['code'] != 0:
                return code_freq[0:i+1]
        return code_freq[0:]

    def __get_project(self, pid):
        project = self._db.collection(
            u'projects').document(pid).get().to_dict()

        return project

    def __get_unique(self, collection):
        return next(collection.stream())


