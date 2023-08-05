
class POPO(object):

    _client = None

    def to_payload(self) -> dict:
        """
        Return a payload suitable for making a POST / PATCH
        :return: dict
        """
        return self.__dict__

    def set_client(self, client):
        """
        Set the GRIP client this object was instantiated from
        Allows convenience methods on resources
        :param client: GRIPClient
        :return:
        """
        self._client = client

    @classmethod
    def from_dict(cls, data: dict):
        """
        Create and populate this object from a dict
        :param data: dict
        :return: POPO
        """
        cont = cls()
        cont.__dict__.update(data)
        return cont
