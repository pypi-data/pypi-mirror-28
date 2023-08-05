#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `ibancom` package."""
from requests.exceptions import ConnectionError

import copy
import mock
import pytest
from ibancom import ibancom

TEST_IBAN = 'DE27100777770209299700'
INVALID_TEST_IBAN = 'DE2710077777020929970043'
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
    "sepa_data": {"SCT": "YES", "SDD": "YES", "COR1": "YES", "B2B": "NO",
                  "SCC": "YES"}
}


def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    data = copy.deepcopy(TEST_IBAN_DATA)

    if kwargs['params']['iban'] != TEST_IBAN:
        data['validations'].append({
            "code": "201",
            "message": "Account Number check digit is incorrect",
        })

    return MockResponse(data, 200)


def mocked_failing_requests_get(*args, **kwargs):
    raise ConnectionError


@mock.patch('requests.get', side_effect=mocked_requests_get)
def test_get_bic(request_get):
    client = ibancom.IBANClient(api_key='FAKE_KEY')
    iban = client.get(iban=TEST_IBAN)
    assert iban.bic == 'NORSDE51'


@mock.patch('requests.get', side_effect=mocked_requests_get)
def test_valid_iban(request_get):
    client = ibancom.IBANClient(api_key='FAKE_KEY')
    iban = client.get(iban=TEST_IBAN)
    assert iban.is_valid()


@mock.patch('requests.get', side_effect=mocked_requests_get)
def test_invalid_iban(request_get):
    client = ibancom.IBANClient(api_key='FAKE_KEY')
    iban = client.get(iban=INVALID_TEST_IBAN)
    assert not iban.is_valid()


@mock.patch('requests.get', side_effect=mocked_failing_requests_get)
def test_iban_exception(request_get):
    client = ibancom.IBANClient(api_key='FAKE_KEY')
    with pytest.raises(ibancom.IBANException):
        client.get(iban=INVALID_TEST_IBAN)


@mock.patch('requests.get', side_effect=mocked_requests_get)
def test_validate_raise_exception(request_get):
    client = ibancom.IBANClient(api_key='FAKE_KEY')
    iban = client.get(iban=INVALID_TEST_IBAN)
    with pytest.raises(ibancom.IBANValidationException):
        iban.validate()


@mock.patch('requests.get', side_effect=mocked_requests_get)
def test_iban_attributes(request_get):
    client = ibancom.IBANClient(api_key='FAKE_KEY')
    iban = client.get(iban=TEST_IBAN)
    assert iban.is_valid()
    assert iban.bank == 'norisbank'
    assert iban.city == 'Berlin'
    assert iban.zip == "10625"
    assert iban.email is None
    assert iban.country == 'Germany'
    assert iban.account == "0209299700"
