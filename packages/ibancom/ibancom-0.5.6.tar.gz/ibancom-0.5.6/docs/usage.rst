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
    # Checking SEPA supports
    iban.supports_sct  # True if account supports SEPA Credit Transfer.
    iban.supports_sdd  # True if account supports SEPA Direct Debit.
    iban.supports_cor1  # True if account supports SEPA COR1.
    iban.supports_b2b  # True if account supports SEPA Business to Business.
    iban.supports_scc  # True if account supports SEPA Card Clearing.
