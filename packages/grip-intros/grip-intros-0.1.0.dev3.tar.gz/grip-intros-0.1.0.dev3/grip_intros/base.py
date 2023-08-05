
class POPO(object):

    def to_payload(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, data):
        cont = cls()
        cont.__dict__.update(data)
        return cont
