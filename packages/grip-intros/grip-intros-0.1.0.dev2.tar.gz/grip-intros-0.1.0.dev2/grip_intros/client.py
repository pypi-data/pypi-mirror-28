import json

import requests

from grip_intros.container import Container
from grip_intros.thing import Thing, Category


class GRIPClient():

    def __init__(self, api_key, test_mode=False):
        self.api_key = api_key
        if test_mode:
            self.base_uri = 'https://api-test.intros.at/1/'
        else:
            self.base_uri = 'https://api.intros.at/1/'

    def build_uri(self, path):
        return "%s%s" % (self.base_uri, path)

    def get_complete_url(self, url_or_path):
        if url_or_path.startswith('http'):
            return url_or_path

        if url_or_path.startswith('/'):
            url_or_path = url_or_path[1:]

        return self.build_uri(url_or_path)

    def get(self, url):
        url = self.get_complete_url(url)
        request = requests.get(url, headers=self.get_headers())
        request.raise_for_status()
        return request.json().get('data')

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
        final_headers = self.get_headers()
        final_headers.update(headers)
        request = requests.delete(url, headers=final_headers)
        request.raise_for_status()
        return request.json()

    def get_headers(self):
        """
        Get headers required to talk to GRIP API

        :return: dict
        """

        return {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer %s' % self.api_key
        }

    def list_containers(self):
        url = self.build_uri('container')
        response = self.get(url)
        return [Container.from_dict(data) for data in response]

    def get_container(self, container_id):
        url = self.build_uri('container/%i' % container_id)
        response = self.get(url)
        return Container.from_dict(response)

    def create_container(self, container):
        url = self.build_uri('container')
        if isinstance(container, Container):
            payload = container.to_payload()
        else:
            payload = container
        response = self.post(url, payload)
        return Container.from_dict(response.get('data'))

    def get_things(self, container_id):
        response = self.get(f'/container/{container_id}/thing')
        return [Thing.from_dict(item) for item in response]

    def get_thing(self, thing_id):
        response = self.get(f'/thing/{thing_id}')
        return Thing.from_dict(response)

    def create_thing(self, thing):
        if isinstance(thing, Thing):
            payload = thing.to_payload()
        else:
            payload = thing

        assert isinstance(payload, dict), \
            'Must supply an instance of grip.thing.Thing or dict'

        url = self.build_uri('thing')
        response = self.post(url, payload)
        return Thing.from_dict(response.get('data'))

    def get_categories(self):
        response = self.get(f'/thing/category')
        return [Category.from_dict(item) for item in response]
