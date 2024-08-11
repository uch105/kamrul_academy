from django.test import TestCase
import requests
import json


# Create your tests here.

SANDBOX_APP_KEY = '8o2NKRBt9DM3n0e6OXkO8eKftc'

SANDBOX_APP_SECRET_KEY = 'xYQO1NscWgNXL52P2pNRDvVFXtcm5IMi8Gx2BCJvFm2wLeV3LnFK'

SANDBOX_USERNAME = '01323314826'

SANDBOX_PASSWORD = '5<I|PK:xdWq'

GRANT_TOKEN_URL = 'https://tokenized.pay.bka.sh/v1.2.0-beta/tokenized/checkout/token/grant'

REFRESH_TOKEN_URL = 'https://tokenized.pay.bka.sh/v1.2.0-beta/tokenized/checkout/token/refresh'

CREATE_PAYMENT_URL = 'https://tokenized.pay.bka.sh/v1.2.0-beta/tokenized/checkout/create'

EXECUTE_PAYMENT_URL = 'https://tokenized.pay.bka.sh/v1.2.0-beta/tokenized/checkout/execute'

QUERY_PAYMENT_URL = 'https://tokenized.pay.bka.sh/v1.2.0-beta/tokenized/checkout/payment/status'

CALL_BACK_URL = 'kamrulacademy.com'


def grant_payment():

    grant_payload = {
        "app_key": SANDBOX_APP_KEY,
        "app_secret": SANDBOX_APP_SECRET_KEY
        }
    grant_headers = {
        "accept": "application/json",
        "username": SANDBOX_USERNAME,
        "password": SANDBOX_PASSWORD,
        "content-type": "application/json"
        }
    grant_response = requests.post(GRANT_TOKEN_URL , json=grant_payload, headers=grant_headers)

    grant_json = grant_response.text
    grant_json_data = json.loads(grant_json)

    id_token = grant_json_data['id_token']
    refresh_token = grant_json_data['refresh_token']

    print(id_token)

    return id_token

grant_payment()