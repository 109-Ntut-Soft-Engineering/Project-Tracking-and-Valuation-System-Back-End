import abc

class Entity(abc.ABC):
    @abc.abstractclassmethod
    @staticmethod
    def from_dict(source):
        return NotImplemented

    def to_dict(self):
        return NotImplemented

    def __repr__(self):
        return ''

