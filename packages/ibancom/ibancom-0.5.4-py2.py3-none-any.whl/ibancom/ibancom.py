# -*- coding: utf-8 -*-

import requests
from requests.exceptions import ConnectionError, HTTPError


class IBANException(Exception):
    pass


class IBANValidationException(Exception):
    pass


class IBAN(object):
    def __init__(self, validation_errors, **data):
        self.validation_errors = validation_errors
        self.__dict__.update(data)

    def is_valid(self):
        return not self.validation_errors

    def validate(self):
        if self.validation_errors:
            raise IBANValidationException(self.validation_errors)


class IBANClient(object):
    def __init__(self, api_key, api_url=None):
        self.api_key = api_key
        self.api_url = api_url or 'https://www.iban.com/clients/api/ibanv2.php'

    def get(self, iban):
        data = self._fetch_data(iban)
        validation_errors = [x for x in data['validations']
                             if not x['code'].startswith('00')]
        return IBAN(validation_errors, **data['bank_data'])

    def _fetch_data(self, iban):
        params = {
            'api_key': self.api_key,
            'format': 'json',
            'iban': iban,
        }
        try:
            response = requests.get(self.api_url, params=params)
        except (HTTPError, ConnectionError):
            raise IBANException('API connection failed.')
        return response.json()
