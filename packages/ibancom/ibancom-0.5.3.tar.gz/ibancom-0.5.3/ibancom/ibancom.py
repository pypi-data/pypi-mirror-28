# -*- coding: utf-8 -*-

import requests
from requests.exceptions import HTTPError, ConnectionError


class IBANException(Exception):
    pass


class IBANClient(object):
    def __init__(self, api_key, iban, api_url=None):
        self.api_key = api_key
        self.api_url = api_url or 'https://www.iban.com/clients/api/ibanv2.php'
        self.iban = iban
        self.data = self.fetch_data()

    def is_valid(self):
        return not any([x for x in self.data['validations']
                        if not x['code'].startswith('00')])

    def fetch_data(self):
        params = {
            'api_key': self.api_key,
            'format': 'json',
            'iban': self.iban,
        }
        try:
            response = requests.get(self.api_url, params=params)
        except (HTTPError, ConnectionError):
            raise IBANException('API connection failed.')
        content = response.json()
        return content

    def get_bic(self):
        return self.data['bank_data']['bic']
