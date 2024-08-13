import requests
import json
from .models import Invoice,Purchased,Enrolled,RecordedCourse,LiveCourse
from .bn_nums import to_bn,to_num
from django.shortcuts import redirect

SANDBOX_APP_KEY = '8o2NKRBt9DM3n0e6OXkO8eKftc'

SANDBOX_APP_SECRET_KEY = 'xYQO1NscWgNXL52P2pNRDvVFXtcm5IMi8Gx2BCJvFm2wLeV3LnFK'

SANDBOX_USERNAME = '01323314826'

SANDBOX_PASSWORD = '5<I|PK:xdWq'

GRANT_TOKEN_URL = 'https://tokenized.pay.bka.sh/v1.2.0-beta/tokenized/checkout/token/grant'

REFRESH_TOKEN_URL = 'https://tokenized.pay.bka.sh/v1.2.0-beta/tokenized/checkout/token/refresh'

CREATE_PAYMENT_URL = 'https://tokenized.pay.bka.sh/v1.2.0-beta/tokenized/checkout/create'

EXECUTE_PAYMENT_URL = 'https://tokenized.pay.bka.sh/v1.2.0-beta/tokenized/checkout/execute/'

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

    return id_token

def create_payment(amount,id_token,invoice_no):
                
    create_payload = {
        "mode": "0011",
        "payerReference": "KamrulAcademy",
        "callbackURL": 'https://kamrulacademy.com/',
        "amount": str(amount),
        "intent": "sale",
        "currency": "BDT",
        "merchantInvoiceNumber": invoice_no,
    }
    create_headers = {
        "accept": "application/json",
        "Authorization": id_token,
        "X-APP-Key": SANDBOX_APP_KEY,
        "content-type": "application/json"
    }
    create_response = requests.post(CREATE_PAYMENT_URL , json=create_payload, headers=create_headers)

    create_json = create_response.text
    create_json_data = json.loads(create_json)
    paymentID = create_json_data["paymentID"]
    bkash_url = create_json_data["bkashURL"]

    invoice = Invoice.objects.get(invoice=invoice_no)
    invoice.paymentID = paymentID
    invoice.save()

    return redirect(bkash_url)

def execute_payment(paymentID):

    try:

        invoice = Invoice.objects.filter(paymentID=paymentID)
        
        execute_payload = {
            "paymentID" : invoice[0].paymentID,#paymentID
        }
        execute_headers = {
            "accept": "application/json",
            "Authorization": invoice[0].id_token,#id_token
            "X-APP-Key": SANDBOX_APP_KEY,
            "content-type": "application/json"
        }

        execute_response = requests.post(EXECUTE_PAYMENT_URL+paymentID , json=execute_payload, headers=execute_headers)

        execute_json = execute_response.text
        if invoice[0].relatedid[:4]=="book":
            bookpurchase = Purchased.objects.get(purchaseid=invoice[0].invoice)
            bookpurchase.status = True
            bookpurchase.save()
        else:
            coursepurchase = Enrolled.objects.get(courseid=invoice[0].relatedid,username=invoice[0].username)
            coursepurchase.status = True
            coursepurchase.save()
            if invoice[0].relatedid[:4]=="live":
                course = LiveCourse.objects.get(courseid=invoice[0].relatedid)
                course.total_student = to_bn(to_num(course.total_student) + 1)
                course.save()
            else:
                course = RecordedCourse.objects.get(courseid=invoice[0].relatedid)
                course.total_student = to_bn(to_num(course.total_student) + 1)
                course.save()
        execute_json_data = json.loads(execute_json)
        try:
            invoice[0].trxID = execute_json_data["trxID"]
        except:
            invoice[0].trxID = "Null"
        invoice[0].status = True
        invoice[0].save()
        return True
    
    except:

        return False