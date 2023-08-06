import clarus.services

def firds(output=None, **params):
    return clarus.services.api_request('MIFID', 'FIRDS', output=output, **params)

