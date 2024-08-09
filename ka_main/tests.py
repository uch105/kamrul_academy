from django.test import TestCase
import requests
import json


# Create your tests here.

SANDBOX_APP_KEY = '4f6o0cjiki2rfm34kfdadl1eqq'

SANDBOX_APP_SECRET_KEY = '2is7hdktrekvrbljjh44ll3d9l1dtjo4pasmjvs5vl5qr3fug4b'

SANDBOX_USERNAME = 'sandboxTokenizedUser02'

SANDBOX_PASSWORD = 'sandboxTokenizedUser02@12345'

GRANT_TOKEN_URL = 'https://tokenized.sandbox.bka.sh/v1.2.0-beta/tokenized/checkout/token/grant'

REFRESH_TOKEN_URL = 'https://tokenized.sandbox.bka.sh/v1.2.0-beta/tokenized/checkout/token/refresh'

CREATE_PAYMENT_URL = 'https://tokenized.sandbox.bka.sh/v1.2.0-beta/tokenized/checkout/create'

EXECUTE_PAYMENT_URL = 'https://tokenized.sandbox.bka.sh/v1.2.0-beta/tokenized/checkout/execute'

QUERY_PAYMENT_URL = 'https://tokenized.sandbox.bka.sh/v1.2.0-beta/tokenized/checkout/payment/status'





execute_payload = {
    "paymentID" : 'TR0011i7bQhzX1710703649435',
}
execute_headers = {
    "accept": "application/json",
    "Authorization": 'eyJraWQiOiJvTVJzNU9ZY0wrUnRXQ2o3ZEJtdlc5VDBEcytrckw5M1NzY0VqUzlERXVzPSIsImFsZyI6IlJTMjU2In0',
    "X-APP-Key": SANDBOX_APP_KEY,
    "content-type": "application/json"
}

execute_response = requests.post(EXECUTE_PAYMENT_URL , json=execute_payload, headers=execute_headers)

execute_json = execute_response.text
print(execute_json)


'''
execute_json_data = json.loads(execute_json)

    trxID = execute_json_data["trxID"]
    try:
        invoice.trxID = trxID
    except:
        return False
    
    transaction_status = execute_json_data["transactionStatus"]
    if transaction_status == "Completed":
        invoice.status = True
        invoice.save()
        return True
    else:
        return False
'''