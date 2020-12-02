from utilities.git_api_requester import GitApiRequester


class ProjectInformationCalculator(object):
    def __init__(self, project, token):
        self.project = project
        self.token = token

    def get_code_freq(self):
        requester = GitApiRequester(self.token)
        code_freqies= []
        for rp_url in self.project.repositories:
            # 用url拿到rp
            rp = requester.get_rp_by_rul(rp_url)
            if rp is None:
                pass
            else:
                # get_stats_code_frequency 可以換成你要的
                # 先不要用get_rp_info 他會撈code_freq, issues, commits會有點久
                code_freq = requester.get_stats_code_frequency(rp)
                code_freqies.append(code_freq)

        code_freq_series = {}
        for rp_code_freq in code_freqies:
            for week_data in rp_code_freq:
                date = week_data['week']
                progress = week_data['additions'] + week_data['deletion']
                if date not in code_freq_series.keys():
                    code_freq_series[date] = progress
                else:
                    code_freq_series += progress
        return code_freq_series




