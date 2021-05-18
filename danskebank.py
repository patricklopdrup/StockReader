import json, requests, creds
from pprint import pprint

class DanskeBank():
    '''
    Documentation for Danske Bank API:
    https://developers.danskebank.com/documentation
    '''

    # Test login [sandbox mode]
    login = creds.dk_bank_test_login
    password = creds.dk_bank_test_password

    # For initial authentication request
    countryCode = "dk"
    channel = "private"
    auth_endpoint = f"https://psd2-auth.danskebank.com/psd2/{countryCode}/{channel}/.well-known/openid-configuration"

    # Store the response from authentication request
    openid_config = {}

    def __init__(self):
        # Request access and save json response
        r = requests.get(self.auth_endpoint)
        self.openid_config = r.json()
        pprint(r.json())


if __name__ == "__main__":
    dk = DanskeBank()


    