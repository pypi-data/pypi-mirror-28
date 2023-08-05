import requests
from grip_intros.container import Container
from grip_intros.thing import Thing, Category


class GRIPClient:

    def __init__(self, api_key, test_mode=False):
        self.api_key = api_key
        if test_mode:
            self.base_uri = 'https://api-test.intros.at/1/'
        else:
            self.base_uri = 'https://api.intros.at/1/'

    def _create_obj(self, cls, data):
        obj = cls.from_dict(data)
        obj.set_client(self)
        return obj

    def build_uri(self, path):
        return "%s%s" % (self.base_uri, path)

    def get_complete_url(self, url_or_path):
        if url_or_path.startswith('http'):
            return url_or_path

        if url_or_path.startswith('/'):
            url_or_path = url_or_path[1:]

        return self.build_uri(url_or_path)

    def get(self, url, headers={}):
        final_headers = self.get_headers()
        final_headers.update(headers)
        url = self.get_complete_url(url)
        request = requests.get(url, headers=final_headers)
        request.raise_for_status()
        return request.json()

    def post(self, url, payload={}, headers={}):
        url = self.get_complete_url(url)
        final_headers = self.get_headers()
        final_headers.update(headers)
        request = requests.post(url, json=payload, headers=final_headers)
        request.raise_for_status()
        return request.json()

    def patch(self, url, payload={}, headers={}):
        url = self.get_complete_url(url)
        final_headers = self.get_headers()
        final_headers.update(headers)
        request = requests.patch(url, json=payload, headers=final_headers)
        request.raise_for_status()
        return request.json()

    def delete(self, url, headers={}):
        url = self.get_complete_url(url)
        final_headers = self.get_headers()
        final_headers.update(headers)
        request = requests.delete(url, headers=final_headers)
        request.raise_for_status()
        return request.json()

    def put(self, url, payload={}, headers={}):
        url = self.get_complete_url(url)
        final_headers = self.get_headers()
        final_headers.update(headers)
        request = requests.put(url, json=payload, headers=final_headers)
        request.raise_for_status()
        return request.json()

    def get_headers(self):
        """
        Get headers required to talk to GRIP API

        :return: dict
        """

        return {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {token}'.format(token=self.api_key)
        }

    def list_containers(self):
        url = self.build_uri('container')
        response = self.get(url)
        data = response.get('data')
        return [self._create_obj(Container, item) for item in data]

    def get_container(self, container_id):
        url = self.build_uri(
            'container/{container_id}'.format(container_id=container_id)
        )
        response = self.get(url)
        return self._create_obj(Container, response.get('data'))

    def create_container(self, container):
        url = self.build_uri('container')
        if isinstance(container, Container):
            payload = container.to_payload()
        else:
            payload = container
        response = self.post(url, payload)
        return self._create_obj(Container, response.get('data'))

    def get_things(self, container_id):
        response = self.get(
            '/container/{container_id}/thing'.format(container_id=container_id)
        )
        return [
            self._create_obj(Thing, item) for item in response.get('data')
        ]

    def get_thing(self, thing_id):
        response = self.get('/thing/{thing_id}'.format(thing_id=thing_id))
        return self._create_obj(Thing, response.get('data'))

    def get_thing_auth_token(self, thing_id, session_source):
        response = self.get(
            '/thing/{thing_id}/token'.format(thing_id=thing_id),
            headers={'session-source': session_source}
        )
        return response.get('data').get('token')

    def _get_thing_data(self, thing_or_dict):
        if isinstance(thing_or_dict, Thing):
            payload = thing_or_dict.to_payload()
        else:
            payload = thing_or_dict

        assert isinstance(payload, dict), \
            'Must supply an instance of grip.thing.Thing or dict'

        return payload

    def create_thing(self, thing):
        payload = self._get_thing_data(thing)
        url = self.build_uri('thing')
        response = self.post(url, payload)
        return self._create_obj(Thing, response.get('data'))

    def update_thing(self, thing_id, thing):
        payload = self._get_thing_data(thing)
        url = self.build_uri('thing/{thing_id}'.format(thing_id=thing_id))
        return self.patch(url, payload)

    def get_categories(self):
        response = self.get('/thing/category')
        return [
            self._create_obj(Category, item) for item in response.get('data')
        ]
