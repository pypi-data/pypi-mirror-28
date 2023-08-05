#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `ibancom` package."""
import mock
import pytest

from ibancom import ibancom

TEST_IBAN = 'DE27100777770209299700'
TEST_IBAN_DATA = {
    "bank_data": {
        "bic": "NORSDE51",
        "branch": None,
        "bank": "norisbank",
        "address": "",
        "city": "Berlin",
        "state": None,
        "zip": "10625",
        "phone": None,
        "fax": None,
        "www": None,
        "email": None,
        "country": "Germany",
        "country_iso": "DE",
        "account": "0209299700"
    },
    "errors": [],
    "validations": [
        {"code": "002", "message": "Account Number check digit is correct"},
        {"code": "001", "message": "IBAN Check digit is correct"},
        {"code": "005", "message": "IBAN structure is correct"},
        {"code": "003", "message": "IBAN Length is correct"}
    ],
    "sepa_data": {"SCT": "YES", "SDD": "YES", "COR1": "YES", "B2B": "NO", "SCC": "YES"}
}


def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    data = TEST_IBAN_DATA.copy()

    if kwargs['params']['iban'] != TEST_IBAN:
        data['validations'].append(
            {"code": "201", "message": "Account Number check digit is incorrect"}
        )

    return MockResponse(data, 200)


@mock.patch('requests.get', side_effect=mocked_requests_get)
def test_get_bic(request_get):
    client = ibancom.IBANClient(
        api_key='FAKE_KEY', iban=TEST_IBAN)
    assert client.get_bic() == 'NORSDE51'


@mock.patch('requests.get', side_effect=mocked_requests_get)
def test_valid_iban(request_get):
    client = ibancom.IBANClient(api_key='FAKE_KEY', iban=TEST_IBAN)
    assert client.is_valid()


@mock.patch('requests.get', side_effect=mocked_requests_get)
def test_invalid_iban(request_get):
    client = ibancom.IBANClient(
        api_key='FAKE_KEY', iban='DE2710077777020929970043')
    assert not client.is_valid()
