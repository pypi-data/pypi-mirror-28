=====
Usage
=====

To use ibancom in a project::

    from ibancom import IBANClient
    client = IBANClient(api_key='YOUR_API_KEY', iban='IBAN_TO_VALIDATE')
    client.is_valid()  # Return True if IBAN is valid
    client.get_bic()  # Return BIC from IBAN
    client.data  # Contains a dictionnary of returned data from the API
