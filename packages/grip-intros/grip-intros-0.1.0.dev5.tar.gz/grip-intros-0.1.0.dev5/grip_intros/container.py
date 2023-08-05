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
