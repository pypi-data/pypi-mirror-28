=====
Usage
=====

To use ibancom in a project::

    from ibancom import IBANClient
    client = IBANClient(api_key='YOUR_API_KEY')
    iban = client.get(iban='IBAN_TO_VALIDATE')
    # IBAN object contains bank data from the API as attributes and validation_errors
    iban.is_valid()  # Return True if IBAN is valid
    iban.validate()  # Will raise an IBANValidationException if invalid
    iban.validation_errors  # Contains list of possible invalid iban criterias
    iban.bic  # BIC of the bank account
    iban.account  # Account number
