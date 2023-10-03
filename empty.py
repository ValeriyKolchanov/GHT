from string import ascii_letters


class Person:

    S_RUS = 'абвгдеёжзийклмнопрстуфхцчшщьыъэюя-'
    S_RUS_UPPER = S_RUS.upper()

    @classmethod
    def validate_fio(cls, fio):
        if not isinstance(fio, str):
            raise TypeError('fio must be string')
        f = fio.split()
        if len(f) != 3:
            raise TypeError('error fio format')
        letters = f'{ascii_letters}{cls.S_RUS}{cls.S_RUS_UPPER}'
        for s in f:
            if len(s) < 1:
                raise TypeError('must be even 1 symbol in fio')
            if len(s.strip(letters)) != 0:
                raise TypeError('must be alpha and _ in fio only')

    @classmethod
    def validate_old(cls, old):
        if not isinstance(old, int) or old < 14 or old > 100:
            raise TypeError('old must be digit in range [14; 100]')

    @classmethod
    def validate_ps(cls, ps):
        if not isinstance(ps, str):
            raise TypeError('ps must be string')
        s = ps.split()
        if len(s) != 2 or len(s[0]) != 4 or len(s[1]) != 6:
            raise TypeError('error ps format')
        for p in s:
            if not p.isdigit():
                raise TypeError('ps must be digit')

    @classmethod
    def validate_weight(cls, weight):
        if not isinstance(weight, float) or weight < 30:
            raise TypeError('error weight format')

    @property
    def fio(self):
        return self.__fio

    @property
    def old(self):
        return self.__old

    @old.setter
    def old(self, old):
        self.validate_old(old=old)
        self.__old = old

    @property
    def ps(self):
        return self.__ps

    @ps.setter
    def ps(self, ps):
        self.validate_ps(ps=ps)
        self.__ps = ps

    @property
    def weight(self):
        return self.__weight

    @weight.setter
    def weight(self, weight):
        self.validate_weight(weight=weight)
        self.__weight = weight

    def __init__(self, fio: str, old: int, ps: str, weight: float):
        self.validate_fio(fio=fio)
        self.__fio = fio
        self.old = old
        self.ps = ps
        self.weight = weight


if __name__ == '__main__':
    p = Person(fio='Ab Bc Cd', old=25, ps='1234 567890', weight=60.0)
    print(p.__dict__)
