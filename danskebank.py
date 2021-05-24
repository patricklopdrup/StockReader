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

    sandbox_endpoint = f"https://sandbox-obp-auth.danskebank.com/sandbox-open-banking/{channel}/.well-known/openid-configuration"

    # Store the response from authentication request
    openid_config = {}
    jwk = {}

    def __init__(self):
        # Request access and save json response
        # r = requests.get(self.auth_endpoint)
        r = requests.get(self.sandbox_endpoint)
        self.openid_config = r.json()
        jwk_response = requests.get(self.openid_config['jwks_uri'])
        self.jwk = jwk_response.json()
        pprint(self.jwk)
        #pprint(r.json())


if __name__ == "__main__":
    dk = DanskeBank()


    