import abc


class Requester(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_commits(self, rp):
        pass

    @abc.abstractmethod
    def get_issues(self, rp):
        pass

    @abc.abstractmethod
    def get_code_freq(self, rp):
        pass