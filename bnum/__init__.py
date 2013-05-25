
import collections, itertools


class BnumMeta(type):

    @classmethod
    def __prepare__(metacls, name, bases):
        return collections.defaultdict(itertools.count().__next__)

    # def __new__(cls, *args, **kargs):
    #     print('gggggggggg')
    #     return super().__new__(cls, *args, **kargs)


class Bnum(object, metaclass=BnumMeta):

    def __new__(cls, *args, **kargs):
        print('dsasadsa')
        return super().__new__(cls, *args, **kargs)

    pass

