from grip_intros.base import POPO


class Container(POPO):

    def __init__(
            self,
            name: str = None,
            description: str = None,
            ref_code: str = None,
            color: str = None,
            type: str = None,
            picture: str = None,
            thumbnail: str = None):
        self.name = name
        self.description = description
        self.ref_code = ref_code
        self.color = color
        self.type = type
        self.picture = picture
        self.thumbnail = thumbnail

    def to_payload(self):
        attrs = [
            'name',
            'description',
            'ref_code',
            'color',
            'type',
            'picture',
            'thumbnail'
        ]
        ret = {}
        for attr in attrs:
            ret[attr] = getattr(self, attr, '')

        return ret

    def add_thing(self, thing_id, data={}):
        """
        Add the thing identified by thing_id to this container
        :param thing_id: int
        :param data: optional registration data (dict)
        :return: response
        """
        assert self._client is not None
        url = "/container/{container_id}/thing/{thing_id}".format(
            container_id=getattr(self, 'id'), thing_id=thing_id
        )
        return self._client.put(url, data)

    def remove_thing(self, thing_id):
        """
        Remove the thing identified by thing_id from this container
        :param thing_id: int
        :return:
        """
        assert self._client is not None
        url = "/container/{container_id}/thing/{thing_id}".format(
            container_id=getattr(self, 'id'), thing_id=thing_id
        )
        return self._client.delete(url)
