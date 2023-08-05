from grip_intros.base import POPO


class Thing(POPO):

    fields = [
        'name',
        'first_name',
        'last_name',
        'email',
        'headline',
        'summary',
        'job_title',
        'company_name',
        'job_industry',
        'gps_lat',
        'gps_lng',
        'location',
        'location_code',
        'categories',
        'picture_url',
        'matches',
        'subjects',
        'type_id',
        'metadata'
    ]

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def to_payload(self):

        assert hasattr(self, 'email') and self.email, \
            "Thing must have an email address"

        result = {}
        for f in self.fields:
            if hasattr(self, f):
                result[f] = getattr(self, f)
        return result

    def get_categories(self):
        assert self._client is not None
        assert hasattr(self, 'id') and isinstance(getattr(self, 'id'), int)
        url = '/thing/{thing_id}/category'.format(thing_id=getattr(self, 'id'))
        response = self._client.get(url)
        data = response.get('data')
        if isinstance(data, dict):
            data = [data]
        return [
            self._client._create_obj(Category, item)
            for item in data
        ]


class Category(POPO):
    pass
